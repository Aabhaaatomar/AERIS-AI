"""
AERIS AI - Conversational Chatbot Service
Orchestrates genuine Google GenAI LLM reasoning connected to:
- Live AQI Service (telemetry across Indian cities and states)
- Historical Data Service (longitudinal CPCB archives)
- ML Prediction Service (trained multi-variate regressors)
- Health Recommendation Service (CPCB-stratified precautions)
- Multi-turn conversation memory & contextual follow-ups
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

# State to major cities mapping for regional queries
STATE_CITY_MAPPING = {
    "haryana": ["Gurgaon", "Faridabad", "Panipat", "Rohtak"],
    "punjab": ["Amritsar", "Ludhiana"],
    "maharashtra": ["Mumbai", "Pune", "Nagpur"],
    "karnataka": ["Bengaluru"],
    "tamil nadu": ["Chennai"],
    "telangana": ["Hyderabad"],
    "gujarat": ["Ahmedabad", "Surat"],
    "rajasthan": ["Jaipur"],
    "west bengal": ["Kolkata"],
    "uttar pradesh": ["Lucknow", "Noida", "Kanpur"],
    "up": ["Lucknow", "Noida", "Kanpur"],
    "delhi": ["Delhi"],
}

# AERIS AI System Prompt
AERIS_SYSTEM_PROMPT = """
You are AERIS AI — an Intelligent Air Quality Assistant.
Tagline: "Understand Your Air. Breathe Smarter."

Your primary role is to assist users with air quality information, pollutant analysis, health recommendations, and atmospheric science with maximum accuracy, conversational naturalness, and clarity.

Core Guidelines:
1. Standards: Base all AQI assessments strictly on the Indian Central Pollution Control Board (CPCB) NAQI scale:
   - 0 - 50: Good (Minimal health impact)
   - 51 - 100: Satisfactory (Minor breathing discomfort to sensitive people)
   - 101 - 200: Moderate (Breathing discomfort to people with asthma/heart disease)
   - 201 - 300: Poor (Breathing discomfort to most people on prolonged exposure)
   - 301 - 400: Very Poor (Respiratory illness on prolonged exposure)
   - 401 - 500: Severe (Affects healthy people, serious impact on vulnerable)

2. Safe Limits (CPCB 24-hr):
   - PM2.5: 60 µg/m³ | PM10: 100 µg/m³ | NO2: 80 µg/m³ | SO2: 80 µg/m³ | CO: 4.0 mg/m³ | O3: 100 µg/m³ (8-hr)

3. Health & Medical Caution:
   - Provide responsible, actionable environmental precautions (e.g. N95/FFP2 masks, indoor HEPA filtration, avoiding early morning smog cardio).
   - Never provide personalized clinical prescriptions. Always advise consulting healthcare professionals for severe personal symptoms.

4. Style & Conversation:
   - Be conversational, friendly, and natural. Greet the user when they say hello.
   - If real-time or historical telemetry is provided in the prompt context, prioritize it directly.
   - If the user asks about a state (like Haryana), clarify that air quality varies across cities, provide available data for major cities in that state (e.g. Gurgaon, Faridabad), and ask which specific city they need.
   - Maintain context across follow-up questions (e.g., if the user previously asked for Delhi and then asks "What about Mumbai?", provide Mumbai's AQI).
   - Format responses in clean, structured Markdown.
"""

class ChatbotService:
    def __init__(self, api_key: Optional[str] = None, provider: str = "gemini", model: Optional[str] = None):
        self.api_key = (api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()
        self.provider = (provider or os.getenv("LLM_PROVIDER", "gemini")).lower()
        self.model = model or os.getenv("LLM_MODEL", "gemini-2.0-flash")
        
        # Sub-services
        self.live_service = LiveAQIService()
        self.historical_service = HistoricalDataService()
        self.prediction_service = PredictionService()
        self.recommendation_service = RecommendationService()
        
        if self.is_configured:
            self.llm_client = LLMClient(api_key=self.api_key, provider=self.provider, model=self.model)
        else:
            self.llm_client = None

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    def extract_context_from_services(self, user_query: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Inspect user question & conversation history to fetch ground-truth domain data from application services.
        """
        context_parts = []
        q = user_query.lower().strip()

        # 0. Contextual resolution for follow-up questions (e.g. "What about Mumbai?")
        target_city = None
        if "what about" in q or "and " in q or "how about" in q:
            for city in config.INDIAN_CITIES:
                if city.lower() in q:
                    target_city = city
                    context_parts.append(f"[CONVERSATION CONTEXT]: Follow-up query detected. User is requesting air quality information for {city.upper()}.")
                    break

        # 1. State-level recognition (e.g. Haryana, Punjab, Maharashtra)
        detected_states = [s for s in STATE_CITY_MAPPING if s in q]
        for state in detected_states:
            cities_in_state = STATE_CITY_MAPPING[state]
            state_data_summary = []
            for c in cities_in_state[:2]:  # Check first 2 key urban hubs
                data = self.live_service.get_city_aqi(c)
                if data:
                    state_data_summary.append(f"{c}: AQI {data['aqi']} ({data['status']}, dominant {data['dominant_pollutant']})")
            
            if state_data_summary:
                context_parts.append(
                    f"[STATE-LEVEL TELEMETRY FOR {state.upper()}]: "
                    f"{state.title()} contains multiple monitoring centers including {', '.join(cities_in_state)}. "
                    f"Current sample telemetry: {'; '.join(state_data_summary)}. "
                    f"Explain that air quality varies across {state.title()} and invite the user to specify their exact city."
                )

        # 2. City recognition & telemetry / historical stats
        detected_cities = [c for c in config.INDIAN_CITIES if c.lower() in q]
        if target_city and target_city not in detected_cities:
            detected_cities.append(target_city)

        for city in detected_cities:
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

            # Historical records
            hist_stats = self.historical_service.get_city_metrics(city)
            if hist_stats and hist_stats.get("record_count", 0) > 0:
                context_parts.append(
                    f"[HISTORICAL ARCHIVE FOR {city.upper()}]: "
                    f"2023-2024 Records: {hist_stats['record_count']} days. "
                    f"Average AQI: {hist_stats['avg_aqi']:.1f}, "
                    f"Peak Spike: {hist_stats['max_aqi']:.1f}."
                )

        # 3. City comparison intent
        if "compare" in q or (" vs " in q and len(detected_cities) >= 2):
            if len(detected_cities) >= 2:
                c1, c2 = detected_cities[0], detected_cities[1]
                d1 = self.live_service.get_city_aqi(c1)
                d2 = self.live_service.get_city_aqi(c2)
                context_parts.append(
                    f"[COMPARATIVE BENCHMARK]: {c1} AQI is {d1['aqi']} ({d1['status']}) vs {c2} AQI is {d2['aqi']} ({d2['status']}). "
                    f"Highlight meteorological and geographic factors (e.g. coastal breeze in Mumbai vs landlocked winter inversion in Delhi)."
                )

        # 4. Pollutant parameter extraction for ML prediction intent
        has_pollutant_vals = bool(re.search(r'(pm2\.?5|pm10|no2|so2|co|o3)\s*(=|:|\s)\s*(\d+)', q))
        if "predict" in q or has_pollutant_vals:
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
            pred_res = self.prediction_service.predict_aqi(features)
            context_parts.append(
                f"[ML PREDICTION ENGINE]: Given parameters {features}, the estimated statistical AQI is {pred_res['estimated_aqi']:.1f} ({pred_res['category']['label']})."
            )

        # 5. Health recommendation intent
        if any(w in q for w in ["safe", "health", "mask", "precaution", "exercise", "asthma", "outdoor", "run", "walk"]):
            context_parts.append(
                "[CPCB HEALTH MATRIX]: "
                "For AQI > 200 (Poor/Very Poor), outdoor cardio should be suspended; "
                "N95/FFP2 masks are recommended; indoor HEPA air filtration advised."
            )

        # 6. Conversation history recall query (e.g. "What did I ask you previously?")
        if "what did i ask" in q or "previous question" in q or "earlier" in q:
            prev_user_queries = []
            if conversation_history:
                for turn in conversation_history:
                    if turn.get("role") == "user":
                        prev_user_queries.append(turn.get("content", ""))
            
            if len(prev_user_queries) >= 1:
                # The turn right before current
                last_q = prev_user_queries[-1]
                context_parts.append(f"[CONVERSATION MEMORY]: The user's previous question was: '{last_q}'. Answer by confirming what they asked.")
            else:
                context_parts.append("[CONVERSATION MEMORY]: This is the beginning of the conversation. No previous questions recorded.")

        if context_parts:
            return "\n\n--- REAL TELEMETRY & SERVICE CONTEXT ---\n" + "\n".join(context_parts) + "\n----------------------------------------\n"
        return ""

    def generate_conversational_response(self, user_query: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Generate an intelligent, highly conversational response using domain services
        when running offline or in demo mode. Never displays a generic static refusal.
        """
        q = user_query.strip().lower()

        # 1. Greetings
        if q in ["hello", "hi", "hey", "good morning", "good evening", "greetings"]:
            return (
                "### 🌬️ Hello! Welcome to AERIS AI\n\n"
                "I am your **Intelligent Air Quality Assistant**. How can I help you understand your air today?\n\n"
                "You can ask me questions like:\n"
                "- *\"What is the current AQI in Delhi?\"*\n"
                "- *\"Explain PM2.5 and why it is dangerous\"*\n"
                "- *\"Haryana AQI\"*\n"
                "- *\"Is it safe to exercise outside?\"*\n"
                "- *\"Compare Delhi and Mumbai air quality\"*"
            )

        # 2. What is AQI?
        if "what is aqi" in q or q == "aqi":
            return (
                "### 📊 Understanding the Air Quality Index (AQI)\n\n"
                "The **Air Quality Index (AQI)** is a standardized numeric scale used by environmental agencies (such as India's **CPCB**) "
                "to report daily air quality and explain how clean or polluted the surrounding air is.\n\n"
                "The overall AQI is calculated based on ambient concentrations of key criteria pollutants: "
                "**PM2.5, PM10, NO₂, SO₂, CO, and O₃**. The pollutant with the highest sub-index determines the day's dominant AQI.\n\n"
                "#### 🏷️ CPCB National AQI Bands:\n\n"
                "| AQI Range | Category | General Health Impact |\n"
                "| :--- | :--- | :--- |\n"
                "| **0 – 50** | 🟢 **Good** | Minimal health impact. Clean and safe air. |\n"
                "| **51 – 100** | 🟡 **Satisfactory** | Minor breathing discomfort to sensitive individuals. |\n"
                "| **101 – 200** | 🟠 **Moderate** | Breathing discomfort to people with asthma, lung, or heart conditions. |\n"
                "| **201 – 300** | 🔴 **Poor** | Breathing discomfort to most people on prolonged exposure. |\n"
                "| **301 – 400** | 🟣 **Very Poor** | Respiratory illness on prolonged exposure. Hazard for children & elderly. |\n"
                "| **401 – 500** | 🟤 **Severe** | Serious health impact on healthy people; severe effects on vulnerable groups. |\n\n"
                "> 💡 *Tip: To check the current AQI for any Indian city, ask 'What is AQI in [City]?'*"
            )

        # 3. What is PM2.5? / Explain PM2.5
        if "pm2.5" in q or "pm 2.5" in q:
            return (
                "### 🔬 What is PM2.5? (Fine Particulate Matter)\n\n"
                "**PM2.5** refers to microscopic particulate matter suspended in the atmosphere with an aerodynamic diameter of **2.5 micrometers or smaller** "
                "— approximately **1/30th the width of a human hair**.\n\n"
                "#### ⚠️ Why is PM2.5 More Dangerous than PM10?\n"
                "1. **Deep Respiratory Penetration**: Unlike coarser particles (**PM10**, such as road dust and pollen) which are largely trapped by nasal hairs and mucus, PM2.5 bypasses upper airway defenses and travels deep into the **alveoli** (lung air sacs).\n"
                "2. **Bloodstream Entry**: Ultra-fine PM2.5 can cross the lung-blood barrier into the circulatory system, triggering systemic inflammation, oxidative stress, and elevated risk of cardiac events.\n"
                "3. **Chemical Toxicity**: PM2.5 particles frequently adsorb heavy metals, polycyclic aromatic hydrocarbons (PAHs), and toxic sulfates on their surfaces.\n\n"
                "#### 📏 Regulatory Thresholds:\n"
                "* **CPCB Standard (24-Hour Average)**: **60 µg/m³**\n"
                "* **CPCB Standard (Annual Average)**: **40 µg/m³**\n"
                "* **WHO Global Guideline (24-Hour)**: **15 µg/m³**\n\n"
                "#### 🏭 Primary Sources:\n"
                "* Vehicular exhaust emissions (especially diesel engines)\n"
                "* Industrial combustion and coal-fired thermal power generation\n"
                "* Seasonal agricultural crop residue (stubble) burning\n"
                "* Municipal solid waste incineration"
            )

        # 4. State query: Haryana AQI
        if "haryana" in q:
            gurgaon_data = self.live_service.get_city_aqi("Gurgaon")
            faridabad_data = self.live_service.get_city_aqi("Faridabad")
            return (
                "### 🌾 Haryana Air Quality Overview\n\n"
                "Air quality in **Haryana** is tracked through CPCB continuous ambient monitoring stations located in key urban and industrial centers across the state. "
                "Because air quality varies significantly depending on proximity to the National Capital Region (NCR), industrial zones, and highway corridors, "
                "here is the latest telemetry for Haryana's major monitoring centers:\n\n"
                f"* **Gurgaon (Gurugram)**: Current AQI is **{gurgaon_data['aqi']}** ({gurgaon_data['status']}), dominant pollutant **{gurgaon_data['dominant_pollutant']}** "
                f"(PM2.5: {gurgaon_data['pollutants'].get('PM2.5', {}).get('value')} µg/m³).\n"
                f"* **Faridabad**: Current AQI is **{faridabad_data['aqi']}** ({faridabad_data['status']}), dominant pollutant **{faridabad_data['dominant_pollutant']}** "
                f"(PM2.5: {faridabad_data['pollutants'].get('PM2.5', {}).get('value')} µg/m³).\n\n"
                "**Which specific city in Haryana would you like detailed telemetry or health recommendations for?**\n"
                "You can specify cities such as **Gurgaon, Faridabad, Panipat, Rohtak, Sonipat, or Karnal**."
            )

        # 5. Is it safe to exercise outside?
        if "exercise" in q or "run" in q or "workout" in q or "outdoor cardio" in q or ("safe" in q and "today" in q):
            return (
                "### 🏃‍♂️ Is It Safe to Exercise Outside Today?\n\n"
                "Whether outdoor exercise is safe depends directly on **current local AQI** and your personal health profile:\n\n"
                "| AQI Band | Safety Level | Guidance for Exercise |\n"
                "| :--- | :--- | :--- |\n"
                "| **0 – 50 (Good)** | ✅ **Safe** | Ideal for all outdoor running, cycling, and sports. |\n"
                "| **51 – 100 (Satisfactory)** | 🟢 **Safe** | Generally safe. Minor sensitivity risk for severe asthmatics. |\n"
                "| **101 – 200 (Moderate)** | ⚠️ **Caution** | Healthy adults can exercise; sensitive individuals should reduce duration and intensity. |\n"
                "| **201 – 300 (Poor)** | ❌ **Unsafe** | Avoid prolonged outdoor cardio. Deep breathing pulls fine particles into lungs. |\n"
                "| **301+ (Very Poor / Severe)** | 🛑 **Hazardous** | **Suspend all outdoor workouts.** Switch to indoor exercise in a HEPA-filtered space. |\n\n"
                "#### 🛡️ Tactical Guidelines for Smoggy Days:\n"
                "1. **Avoid Morning Smog**: Never run during dawn or early morning hours during winter. Surface thermal inversion traps peak pollutants closest to ground level.\n"
                "2. **Mid-Afternoon Window**: If you must exercise outside, choose 1:00 PM – 4:00 PM when solar heating and thermal updrafts disperse ground-level smog.\n"
                "3. **Hydration**: Drink sufficient fluids to maintain mucosal lining moisture and assist natural particle clearance.\n\n"
                "*To check safety for your specific location, ask: 'What is current AQI in [Your City]?'*"
            )

        # 6. City comparison: Delhi vs Mumbai
        if ("delhi" in q and "mumbai" in q) or ("compare" in q and "mumbai" in q):
            delhi = self.live_service.get_city_aqi("Delhi")
            mumbai = self.live_service.get_city_aqi("Mumbai")
            return (
                f"### ⚖️ City Comparison: Delhi vs Mumbai\n\n"
                f"| Parameter | Delhi | Mumbai | Geographical Note |\n"
                f"| :--- | :--- | :--- | :--- |\n"
                f"| **Current AQI** | **{delhi['aqi']}** ({delhi['status']}) | **{mumbai['aqi']}** ({mumbai['status']}) | Delhi air is currently more degraded |\n"
                f"| **Dominant Pollutant** | {delhi['dominant_pollutant']} | {mumbai['dominant_pollutant']} | PM2.5 dominates in northern plains |\n"
                f"| **PM2.5 Concentration** | {delhi['pollutants'].get('PM2.5', {}).get('value')} µg/m³ | {mumbai['pollutants'].get('PM2.5', {}).get('value')} µg/m³ | Primary fine particulate risk |\n"
                f"| **PM10 Concentration** | {delhi['pollutants'].get('PM10', {}).get('value')} µg/m³ | {mumbai['pollutants'].get('PM10', {}).get('value')} µg/m³ | Coarse dust & transport emission |\n\n"
                "#### 🌍 Atmospheric Science Context:\n"
                "* **Mumbai's Coastal Advantage**: Situated on the Arabian Sea, Mumbai benefits from regular diurnal **land and sea breezes** that ventilate urban air and disperse airborne particles.\n"
                "* **Delhi's Landlocked Inversion**: Delhi sits in a landlocked basin flanked by the Indo-Gangetic plains. During winter, cool stagnant air, shallow planetary boundary layers, and low wind speeds trap regional vehicular and biomass emissions near the surface."
            )

        # 7. City queries (Delhi, Bengaluru, Kolkata, Chennai, etc.)
        for city in config.INDIAN_CITIES:
            if city.lower() in q and ("aqi" in q or "air" in q or "status" in q or "pollution" in q):
                data = self.live_service.get_city_aqi(city)
                hist = self.historical_service.get_city_metrics(city)
                return (
                    f"### 🌫️ {city} Air Quality Telemetry\n\n"
                    f"* **Current AQI**: **{data['aqi']}**\n"
                    f"* **CPCB Category**: **{data['status']}**\n"
                    f"* **Dominant Pollutant**: **{data['dominant_pollutant']}**\n"
                    f"* **Last Telemetry Sync**: {data['timestamp']}\n\n"
                    f"#### 🔬 Pollutant Concentrations:\n"
                    f"* **PM2.5**: {data['pollutants'].get('PM2.5', {}).get('value')} µg/m³ (CPCB Standard: 60 µg/m³)\n"
                    f"* **PM10**: {data['pollutants'].get('PM10', {}).get('value')} µg/m³ (CPCB Standard: 100 µg/m³)\n"
                    f"* **NO₂**: {data['pollutants'].get('NO2', {}).get('value')} µg/m³ (CPCB Standard: 80 µg/m³)\n"
                    f"* **CO**: {data['pollutants'].get('CO', {}).get('value')} mg/m³ (CPCB Standard: 4.0 mg/m³)\n\n"
                    f"#### 🏛️ CPCB 2-Year Archive Context:\n"
                    f"Across 2023–2024, {city} averaged **{hist.get('avg_aqi', 0):.1f} AQI** with a historical peak of **{hist.get('max_aqi', 0):.1f} AQI**.\n\n"
                    f"#### 🛡️ Health Guidance:\n"
                    f"{'Air quality is in healthy range for all outdoor activities.' if data['aqi'] <= 100 else 'Sensitive groups (children, elderly, respiratory patients) should avoid prolonged outdoor exposure and use an N95 mask if outdoors.'}"
                )

        # 8. Follow-up: "What about [City]?"
        if ("what about" in q or "and " in q) and any(c.lower() in q for c in config.INDIAN_CITIES):
            for city in config.INDIAN_CITIES:
                if city.lower() in q:
                    data = self.live_service.get_city_aqi(city)
                    return (
                        f"### 📡 Air Quality Status for {city}\n\n"
                        f"Continuing our conversation, here is the current telemetry for **{city}**:\n\n"
                        f"* **Current AQI**: **{data['aqi']}** ({data['status']})\n"
                        f"* **Dominant Pollutant**: **{data['dominant_pollutant']}**\n"
                        f"* **PM2.5 Level**: {data['pollutants'].get('PM2.5', {}).get('value')} µg/m³\n"
                        f"* **PM10 Level**: {data['pollutants'].get('PM10', {}).get('value')} µg/m³\n\n"
                        f"Would you like to compare {city} with your previously queried city, or see health precautions?"
                    )

        # 9. Memory Recall: "What did I ask you previously?"
        if "what did i ask" in q or "previous question" in q or "earlier" in q:
            prev_user_queries = []
            if conversation_history:
                for turn in conversation_history:
                    if turn.get("role") == "user":
                        prev_user_queries.append(turn.get("content", ""))
            
            if prev_user_queries:
                last_q = prev_user_queries[-1]
                return (
                    f"### 🧠 Conversation Memory Recall\n\n"
                    f"In our conversation history, your previous query was:\n\n"
                    f"> **\"{last_q}\"**\n\n"
                    "I track all dialogue turns within our current session state so we can explore follow-up questions seamlessly!"
                )
            else:
                return (
                    "### 🧠 Conversation Memory\n\n"
                    "This is the start of our current session. I haven't recorded any previous questions yet. "
                    "Ask me anything about air quality, city telemetry, or health recommendations!"
                )

        # 10. General conversational fallback with domain knowledge
        return (
            f"### 🤖 AERIS AI Assistant\n\n"
            f"I have received your query regarding **\"{user_query}\"**.\n\n"
            "Here is how I can assist:\n"
            "* **City Telemetry**: Ask for real-time measurements across Indian cities (e.g., Delhi, Mumbai, Bengaluru, Gurgaon, etc.).\n"
            "* **Pollutant Science**: Ask for detailed breakdowns of PM2.5, PM10, NO₂, SO₂, CO, or Ozone.\n"
            "* **Health Advisories**: Ask about outdoor exercise safety, mask recommendations (N95/FFP2), or indoor air purification.\n"
            "* **ML Prediction**: Provide pollutant values (e.g. *\"PM2.5=120, PM10=210\"*) to calculate predictive AQI.\n\n"
            "Feel free to ask a specific question!"
        )

    def process_message(
        self,
        user_query: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        force_demo: bool = False
    ) -> Dict[str, Any]:
        """
        Process the message through genuine Gemini LLM or labeled conversational simulator.
        
        Returns:
            dict: {
                "content": str,
                "is_demo": bool,
                "model": str,
                "error": Optional[str]
            }
        """
        # If API key is missing
        if not self.is_configured:
            conv_resp = self.generate_conversational_response(user_query, conversation_history)
            notice = (
                "<div style='background: rgba(34, 211, 238, 0.08); border: 1px solid rgba(34, 211, 238, 0.25); "
                "border-radius: 8px; padding: 0.5rem 0.75rem; margin-bottom: 0.65rem;'>"
                "<span style='font-size: 0.75rem; color: #22D3EE; font-weight: 700;'>"
                "ℹ️ DEMO RESPONSE • AERIS AI • OFFLINE CONVERSATIONAL SIMULATOR (Configure Gemini API Key in sidebar for live AI)</span></div>"
            )
            return {
                "content": f"{notice}\n\n{conv_resp}",
                "is_demo": True,
                "model": "Offline Simulator",
                "error": None
            }

        # If user explicitly enabled Force Demo Mode
        if force_demo:
            conv_resp = self.generate_conversational_response(user_query, conversation_history)
            tag = '<span class="demo-tag">DEMO RESPONSE • DEMO MODE • OFFLINE SIMULATOR</span>'
            return {
                "content": f"{tag}\n\n{conv_resp}",
                "is_demo": True,
                "model": "Demo Simulator",
                "error": None
            }

        # Genuine AI Mode: Enrich prompt with ground-truth service context
        service_context = self.extract_context_from_services(user_query, conversation_history)
        augmented_prompt = user_query
        if service_context:
            augmented_prompt = f"{user_query}\n\n{service_context}"

        # Clean conversation history
        cleaned_history = []
        if conversation_history:
            for item in conversation_history:
                clean_text = re.sub(r'<[^>]+>', '', item.get("content", "")).strip()
                if clean_text:
                    cleaned_history.append({
                        "role": item.get("role", "user"),
                        "content": clean_text
                    })

        # Call LLM client
        res = self.llm_client.generate(
            prompt=augmented_prompt,
            conversation_history=cleaned_history,
            system_instruction=AERIS_SYSTEM_PROMPT
        )

        if res["success"]:
            # Format with genuine AI badge
            provider_tag = (
                f'<span class="demo-tag" style="background: rgba(16, 185, 129, 0.15); '
                f'border: 1px solid rgba(16, 185, 129, 0.4); color: #10B981;">'
                f'⚡ GENUINE AI RESPONSE • {res["model"].upper()}</span>'
            )
            formatted_content = f"{provider_tag}\n\n{res['text']}"
            return {
                "content": formatted_content,
                "is_demo": False,
                "model": res["model"],
                "error": None
            }
        else:
            # Genuine API Error encountered - Display clear, dedicated error message
            err_msg = res.get("error", "Unknown error contacting Gemini API.")
            err_type = res.get("error_type", "API_ERROR")
            
            error_banner = f"""
<div style="background: rgba(239, 68, 68, 0.12); border: 1px solid #EF4444; border-radius: 10px; padding: 0.85rem; margin-bottom: 0.75rem;">
    <strong style="color: #EF4444;">⚠️ Gemini API Error ({err_type}) / LLM API Error:</strong>
    <p style="margin: 0.25rem 0 0 0; color: #F8FAFC; font-size: 0.85rem;">{err_msg}</p>
    <p style="margin: 0.35rem 0 0 0; color: #94A3B8; font-size: 0.75rem;">Please verify your Gemini API key in sidebar under <strong>⚙️ AI Engine Settings</strong>.</p>
</div>
"""
            fallback_resp = self.generate_conversational_response(user_query, conversation_history)
            return {
                "content": f"{error_banner}\n\n{fallback_resp}",
                "is_demo": True,
                "model": "Fallback Simulator",
                "error": err_msg
            }
