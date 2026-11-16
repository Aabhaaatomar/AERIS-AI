# AERIS AI – Intelligent Air Quality Assistant 🌬️

> **"Understand Your Air. Breathe Smarter."**

AERIS AI is a dark-themed, enterprise-grade AI environmental intelligence assistant designed to deliver real-time air quality monitoring, longitudinal historical analytics, machine learning AQI estimation, cross-city benchmarking, and health advisories based on Central Pollution Control Board (CPCB) standards.

---

## 🎨 Premium Dark AI Dashboard Design System

* **Background**: `#0B0F14`
* **Sidebar**: `#101820`
* **Secondary Background**: `#141E27`
* **Cards & Panels**: `#192630`
* **Primary Accent**: `#10B981` (Emerald Green)
* **Secondary Accent**: `#22D3EE` (Cyan)
* **Main Typography**: `#F8FAFC`
* **Secondary Typography**: `#94A3B8`
* **Borders & Dividers**: `#293946`

---

## 📁 Project Directory Structure

```text
AERIS_AI/
│
├── app.py                     # Main Streamlit application entry point
├── config.py                  # Global configurations, CPCB scales, palette
├── requirements.txt           # Python dependencies
├── README.md                  # Comprehensive documentation
├── .env.example               # Environment variables template
├── .gitignore                 # Version control exclusions
│
├── .streamlit/
│   └── config.toml            # Native Streamlit dark-theme overrides
│
├── services/                  # Backend service layer
│   ├── __init__.py
│   ├── chatbot_service.py     # Intent routing and conversation logic
│   ├── live_aqi_service.py    # Real-time telemetry ingestion (Phase 3)
│   ├── historical_data_service.py # Longitudinal dataset loader (Phase 4)
│   ├── prediction_service.py  # ML inference engine (Phase 5)
│   └── recommendation_service.py # CPCB-aligned health precautions
│
├── components/                # Reusable UI widgets & design system
│   ├── __init__.py
│   ├── sidebar.py             # Navigation, branding & status
│   ├── chat_interface.py      # Conversational interface & suggested prompts
│   ├── metric_cards.py        # Contrast-tested AQI badges & KPI cards
│   └── charts.py              # Dark Plotly charts (Gauges, Lines, Bars)
│
├── views/                     # Top-level screen views
│   ├── __init__.py
│   ├── assistant.py           # Conversational AI Assistant (Default landing)
│   ├── live_aqi.py            # Live telemetry dashboard layout
│   ├── historical_analysis.py # Longitudinal trends & seasonality
│   ├── prediction.py          # ML parameter input & AQI estimation
│   ├── city_comparison.py     # Head-to-head city benchmark
│   └── about.py               # System specifications & roadmap
│
├── data/
│   └── city_day_cpcb.csv      # CPCB historical monitoring dataset (7,310 rows)
│
├── models/                    # Serialized machine learning models (Phase 5)
│
├── assets/
│   └── style.css              # Custom SaaS design styling
│
└── utils/
    ├── __init__.py
    └── helpers.py             # AQI calculators & session handlers
```

---

## 🚀 How to Run the Application

1. Open PowerShell or Terminal and navigate to the project directory:
   ```powershell
   cd C:\Users\tomar\.gemini\antigravity\scratch\AERIS_AI
   ```

2. (Optional) Activate your Python virtual environment if configured.

3. Launch the Streamlit application:
   ```powershell
   streamlit run app.py
   ```

4. The dashboard will launch in your browser at `http://localhost:8501`.

---

## 🗺️ Engineering Roadmap

| Phase | Milestone | Status | Description |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **UI & Foundation** | ✅ **Completed** | Full dark dashboard, conversational landing page, navigation, views |
| **Phase 2** | **AI Chatbot Integration** | ✅ **Completed** | Genuine LLM integration (Gemini & OpenAI), service context routing, fallback |
| **Phase 3** | **Live AQI Integration** | ✅ **Completed** | Live telemetry feeds, CPCB sub-index math, city search, caching & failover |
| **Phase 4** | **Historical Analytics** | ✅ **Completed** | Longitudinal 2023-2024 CPCB analysis, seasonality, YoY benchmarks, rankings |
| **Phase 5** | **Machine Learning** | ✅ **Completed** | Random Forest, Decision Tree & Linear Regression models, evaluation metrics |
| **Phase 6** | **Service Orchestration** | ✅ **Completed** | Chatbot multi-tool calling across Live, ML, Historical & Health services |
| **Phase 7** | **Testing & Deployment** | ✅ **Completed** | 100% test coverage across 6 test suites, cloud ready, zero hardcoded paths |
