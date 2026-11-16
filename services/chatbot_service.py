"""
AERIS AI - Chatbot Service
Modular orchestration service connecting conversational AI to:
- Live AQI service
- Historical data service
- ML prediction service
- Health recommendation service
"""
import os
import re
from typing import List, Dict, Any, Optional

import config
from services.llm_client import LLMClient
from services.live_aqi_service import LiveAQIService
from services.historical_data_service import HistoricalDataService
from services.prediction_service import PredictionService
from services.recommendation_service import RecommendationService
from components.chat_interface import get_demo_response

# AERIS AI System Prompt
AERIS_SYSTEM_PROMPT = """
You are AERIS AI — an Intelligent Air Quality Assistant.
Tagline: "Understand Your Air. Breathe Smarter."

Your primary role is to assist users with air quality information, pollutant analysis, health recommendations, and environmental science with maximum accuracy and clarity.

Core Guidelines:
1. Standards: Base all AQI assessments strictly on the Indian Central Pollution Control Board (CPCB) NAQI scale:
   - 0 - 50: Good (Minimal impact)
   - 51 - 100: Satisfactory (Minor breathing discomfort to sensitive people)
   - 101 - 200: Moderate (Breathing discomfort to people with asthma/heart disease)
   - 201 - 300: Poor (Breathing discomfort to most people on prolonged exposure)
   - 301 - 400: Very Poor (Respiratory illness on prolonged exposure)
   - 401 - 500: Severe (Affects healthy people, serious impact on vulnerable)

2. Safe Limits (CPCB 24-hr):
   - PM2.5: 60 µg/m³ | PM10: 100 µg/m³ | NO2: 80 µg/m³ | SO2: 80 µg/m³ | CO: 4.0 mg/m³ | O3: 100 µg/m³ (8-hr)

3. Health & Medical Caution:
   - Provide responsible, actionable environmental precautions (e.g. N95 masks, indoor HEPA filtration, avoiding early morning smog cardio).
   - Never provide personalized medical diagnoses or clinical prescriptions. Always advise consulting healthcare professionals for personal symptoms.

4. Style:
   - Format responses in clean, structured Markdown (use bullet points, tables, bold key metrics).
   - Keep answers concise, factual, and informative.
   - If real-time or historical telemetry is provided in the prompt context, prioritize it directly.
"""

class ChatbotService:
    def __init__(self, api_key: Optional[str] = None, provider: str = "gemini", model: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.provider = provider or os.getenv("LLM_PROVIDER", "gemini")
        self.model = model or os.getenv("LLM_MODEL", "gemini-1.5-flash")
        
        # Sub-services
        self.live_service = LiveAQIService()
        self.historical_service = HistoricalDataService()
        self.prediction_service = PredictionService()
        self.recommendation_service = RecommendationService()
        
        if self.api_key:
            self.llm_client = LLMClient(api_key=self.api_key, provider=self.provider, model=self.model)
        else:
            self.llm_client = None

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    def extract_context_from_services(self, user_query: str) -> str:
        """
        Inspect the user question and fetch ground-truth domain data from application services.
        """
        context_parts = []
        q = user_query.lower()
        
        # 1. City recognition & telemetry / historical stats
        detected_cities = [c for c in config.INDIAN_CITIES if c.lower() in q]
        for city in detected_cities:
            # Check current atmospheric telemetry
            live_data = self.live_service.get_city_aqi(city)
            if live_data:
                context_parts.append(
                    f"[CURRENT TELEMETRY FOR {city.upper()}]: "
                    f"AQI: {live_data['aqi']} ({live_data['dominant_pollutant']} dominant). "
                    f"PM2.5: {live_data['pollutants'].get('PM2.5', {}).get('value')} µg/m³, "
                    f"PM10: {live_data['pollutants'].get('PM10', {}).get('value')} µg/m³, "
                    f"NO2: {live_data['pollutants'].get('NO2', {}).get('value')} µg/m³, "
                    f"Status: {live_data['status']}, Timestamp: {live_data['timestamp']}."
                )

            # Check historical records
            hist_stats = self.historical_service.get_city_metrics(city)
            if hist_stats and hist_stats.get("record_count", 0) > 0:
                context_parts.append(
                    f"[HISTORICAL ARCHIVE FOR {city.upper()}]: "
                    f"2023-2024 Records: {hist_stats['record_count']} days. "
                    f"Average AQI: {hist_stats['avg_aqi']:.1f}, "
                    f"Max AQI: {hist_stats['max_aqi']:.1f}, "
                    f"Min AQI: {hist_stats['min_aqi']:.1f}."
                )

        # 2. Pollutant parameter extraction for ML prediction intent
        has_pollutant_vals = bool(re.search(r'(pm2\.?5|pm10|no2|so2|co|o3)\s*(=|:|\s)\s*(\d+)', q))
        if "predict" in q or has_pollutant_vals:
            # Try to extract numbers
            pm25_match = re.search(r'pm2\.?5\s*(=|:|\s)\s*(\d+(\.\d+)?)', q)
            pm10_match = re.search(r'pm10\s*(=|:|\s)\s*(\d+(\.\d+)?)', q)
            no2_match = re.search(r'no2\s*(=|:|\s)\s*(\d+(\.\d+)?)', q)
            co_match = re.search(r'co\s*(=|:|\s)\s*(\d+(\.\d+)?)', q)
            
            features = {
                "PM2.5": float(pm25_match.group(2)) if pm25_match else 120.0,
                "PM10": float(pm10_match.group(2)) if pm10_match else 200.0,
                "NO2": float(no2_match.group(2)) if no2_match else 45.0,
                "CO": float(co_match.group(2)) if co_match else 2.0,
            }
            estimated_val = self.prediction_service.predict_aqi(features)
            context_parts.append(
                f"[ML PREDICTION ENGINE]: Given parameters {features}, the estimated statistical AQI is {estimated_val}."
            )

        # 3. Health recommendation intent
        if any(w in q for w in ["safe", "health", "mask", "precaution", "exercise", "asthma", "outdoor", "run"]):
            context_parts.append(
                "[CPCB HEALTH MATRIX]: For AQI > 200 (Poor/Very Poor), outdoor cardio should be suspended; "
                "N95/FFP2 masks are recommended; indoor HEPA air filtration advised."
            )

        if context_parts:
            return "\n\n--- REAL TELEMETRY & SERVICE CONTEXT ---\n" + "\n".join(context_parts) + "\n----------------------------------------\n"
        return ""

    def process_message(
        self,
        user_query: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        force_demo: bool = False
    ) -> Dict[str, Any]:
        """
        Process the message through genuine LLM or labeled demo mode.
        
        Returns:
            dict: {
                "content": str,
                "is_demo": bool,
                "model": str,
                "error": Optional[str]
            }
        """
        # If API key is missing or force_demo is True -> Demo Simulator
        if not self.is_configured or force_demo:
            demo_text = get_demo_response(user_query)
            return {
                "content": demo_text,
                "is_demo": True,
                "model": "Demo Simulator",
                "error": None
            }

        # Otherwise, invoke genuine LLM with service context
        service_context = self.extract_context_from_services(user_query)
        augmented_prompt = user_query
        if service_context:
            augmented_prompt = f"{user_query}\n\n{service_context}"

        # Clean conversation history to pass to LLM (remove demo tags and internal metadata)
        cleaned_history = []
        if conversation_history:
            for item in conversation_history:
                # clean out HTML tags if present
                clean_text = re.sub(r'<[^>]+>', '', item.get("content", ""))
                cleaned_history.append({
                    "role": item.get("role", "user"),
                    "content": clean_text
                })

        res = self.llm_client.generate(
            prompt=augmented_prompt,
            conversation_history=cleaned_history,
            system_instruction=AERIS_SYSTEM_PROMPT
        )

        if res["success"]:
            # Format with genuine AI badge
            provider_tag = f'<span class="demo-tag" style="background: rgba(16, 185, 129, 0.15); border-color: rgba(16, 185, 129, 0.4); color: #10B981;">⚡ LIVE AI • {res["model"].upper()}</span>'
            formatted_content = f"{provider_tag}\n\n{res['text']}"
            return {
                "content": formatted_content,
                "is_demo": False,
                "model": res["model"],
                "error": None
            }
        else:
            # Genuine API Error encountered
            err_msg = res.get("error", "Unknown error contacting LLM API.")
            error_banner = f"""
<div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #EF4444; border-radius: 10px; padding: 0.85rem; margin-bottom: 0.75rem;">
    <strong style="color: #EF4444;">⚠️ LLM API Error ({res.get('error_type', 'API_ERROR')}):</strong>
    <p style="margin: 0.25rem 0 0 0; color: #F8FAFC; font-size: 0.85rem;">{err_msg}</p>
    <p style="margin: 0.35rem 0 0 0; color: #94A3B8; font-size: 0.75rem;">Falling back to verified offline demo response below for continuous operation.</p>
</div>
"""
            fallback_demo = get_demo_response(user_query)
            return {
                "content": f"{error_banner}\n{fallback_demo}",
                "is_demo": True,
                "model": "Fallback Simulator",
                "error": err_msg
            }
