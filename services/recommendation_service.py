"""
AERIS AI - Health Recommendation Service
Generates responsible, evidence-based lifestyle and activity precautions based on AQI categories.
"""
from utils.helpers import get_aqi_category

class RecommendationService:
    @staticmethod
    def get_recommendations(aqi_val: float) -> dict:
        cat = get_aqi_category(aqi_val)
        label = cat["label"]
        
        recommendations = {
            "category": label,
            "color": cat["color"],
            "outdoor_activity": "",
            "exercise": "",
            "mask_guidance": "",
            "sensitive_groups": "",
            "indoor_guidance": "",
            "disclaimer": "General environmental guidance only. Consult a qualified medical practitioner for personalized healthcare decisions."
        }
        
        if label == "Good":
            recommendations["outdoor_activity"] = "Air quality is ideal for all outdoor activities and recreation."
            recommendations["exercise"] = "No restrictions on intense outdoor cardiovascular workouts."
            recommendations["mask_guidance"] = "No respiratory protection required."
            recommendations["sensitive_groups"] = "Safe for infants, elderly, and individuals with respiratory conditions."
            recommendations["indoor_guidance"] = "Natural ventilation and open windows encouraged."
        elif label == "Satisfactory":
            recommendations["outdoor_activity"] = "Normal outdoor recreation is generally safe."
            recommendations["exercise"] = "Outdoor exercise is safe for most healthy individuals."
            recommendations["mask_guidance"] = "Masks optional; sensitive individuals may consider in dusty zones."
            recommendations["sensitive_groups"] = "Extremely sensitive individuals should monitor minor breathing discomfort."
            recommendations["indoor_guidance"] = "Ventilation is safe."
        elif label == "Moderate":
            recommendations["outdoor_activity"] = "Take occasional breaks during prolonged outdoor exertion."
            recommendations["exercise"] = "Consider reducing duration of intense outdoor cardio if experiencing discomfort."
            recommendations["mask_guidance"] = "N95 masks advised near high-traffic traffic intersections."
            recommendations["sensitive_groups"] = "People with asthma, COPD, or heart disease should keep medications handy."
            recommendations["indoor_guidance"] = "Keep windows closed during peak morning traffic rush hours."
        elif label == "Poor":
            recommendations["outdoor_activity"] = "Avoid prolonged or heavy outdoor exertion."
            recommendations["exercise"] = "Shift workouts indoors or to early afternoon when smog levels dip."
            recommendations["mask_guidance"] = "Wear a well-fitted N95 / FFP2 mask when stepping outside."
            recommendations["sensitive_groups"] = "Children, seniors, and respiratory patients should remain indoors."
            recommendations["indoor_guidance"] = "Run indoor HEPA air purifiers; keep doors and windows shut."
        elif label == "Very Poor":
            recommendations["outdoor_activity"] = "Minimize all non-essential outdoor trips."
            recommendations["exercise"] = "Strictly avoid outdoor jogging, cycling, or strenuous physical activity."
            recommendations["mask_guidance"] = "N95/FFP2 respirator mask is mandatory outdoors."
            recommendations["sensitive_groups"] = "High risk of acute respiratory distress. Avoid all outdoor exposure."
            recommendations["indoor_guidance"] = "Seal doors/windows; run air purifiers on high efficiency."
        else: # Severe
            recommendations["outdoor_activity"] = "EMERGENCY CONDITIONS: Stay indoors. Cancel all outdoor activities."
            recommendations["exercise"] = "Zero outdoor physical exertion. Keep physical activity minimal even indoors."
            recommendations["mask_guidance"] = "N95/FFP3 respirator mask required even for brief stepping out."
            recommendations["sensitive_groups"] = "Severe health hazard. High risk of cardiovascular and pulmonary events."
            recommendations["indoor_guidance"] = "Operate HEPA purifiers continuously. Avoid cooking fumes or indoor combustion."

        return recommendations
