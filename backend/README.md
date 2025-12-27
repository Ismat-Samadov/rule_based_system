# Yonca Rule-Based Advisory API

**Azərbaycan kənd təsərrüfatı üçün qayda əsaslı məsləhət sistemi**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)

## 📑 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [📖 API Documentation](#-api-documentation)
- [🏗️ Architecture Diagrams](#️-architecture-diagrams)
  - [API Structure](#api-structure)
  - [Rule Engine Processing Flow](#rule-engine-processing-flow)
  - [Chatbot Interaction Flow](#chatbot-interaction-flow)
- [🔗 Endpoints](#-endpoints)
  - [Recommendations](#recommendations)
  - [Farms & Profiles](#farms--profiles)
  - [Rules](#rules)
  - [Constants](#constants)
  - [Weather Auto-Fetch](#weather-auto-fetch)
  - [Chatbot (Gemini AI)](#chatbot-gemini-ai)
  - [System](#system)
- [📝 Example Usage](#-example-usage)
- [🏗️ Project Structure](#️-project-structure)
  - [Data Structure Organization](#data-structure-organization)
- [📊 Statistics](#-statistics)
- [🔧 Configuration](#-configuration)

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --port 8000

# Or use the run script
./run.sh
```

## 📖 API Documentation

Server işə düşdükdən sonra:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🏗️ Architecture Diagrams

### API Structure

```mermaid
graph TB
    subgraph "FastAPI Application"
        Main[main.py - FastAPI App]

        subgraph "Routers"
            API[api/routes.py]
            Chat[chatbot/routes.py]
        end

        subgraph "Services"
            RE[Rule Engine]
            RL[Rule Loader]
            WS[Weather Service]
            GE[Gemini Engine]
        end

        subgraph "Models"
            Schema[Pydantic Schemas]
            Enums[Enums - FarmType, Region, Urgency]
        end

        subgraph "Data Layer"
            Rules[(127 Rules JSON)]
            Constants[(Constants)]
            Profiles[(Farm Profiles)]
        end
    end

    Main --> API
    Main --> Chat

    API --> RE
    API --> WS
    Chat --> GE

    RE --> RL
    RL --> Rules
    RL --> Constants
    RL --> Profiles

    RE --> Schema
    WS --> Schema
    GE --> Schema

    style Main fill:#fff59d
    style RE fill:#ffccbc
    style GE fill:#f8bbd0
    style Rules fill:#d1c4e9
    style Schema fill:#c8e6c9
```

### Rule Engine Processing Flow

```mermaid
stateDiagram-v2
    [*] --> ReceiveRequest: POST /api/v1/recommendations

    ReceiveRequest --> ValidateInput: Pydantic Validation
    ValidateInput --> LoadRules: Get Farm Type Rules

    LoadRules --> BuildContext: Create Context Dict
    BuildContext --> EvaluateRules: For Each Rule

    state EvaluateRules {
        [*] --> CheckEnabled
        CheckEnabled --> CheckApplicable: If Enabled
        CheckApplicable --> EvaluateConditions: If Applicable

        state EvaluateConditions {
            [*] --> CheckOperator
            CheckOperator --> AND_Logic: AND
            CheckOperator --> OR_Logic: OR

            AND_Logic --> AllTrue: All Match?
            OR_Logic --> AnyTrue: Any Match?

            AllTrue --> [*]: Yes → Match
            AnyTrue --> [*]: Yes → Match
            AllTrue --> [*]: No → Skip
            AnyTrue --> [*]: No → Skip
        }

        EvaluateConditions --> BuildAction: If Matched
        BuildAction --> [*]
    }

    EvaluateRules --> SortResults: All Rules Processed
    SortResults --> GroupByUrgency: Sort by Score

    GroupByUrgency --> GenerateSchedule: Priority Groups Created
    GenerateSchedule --> CreateSummary: Time Slots Assigned
    CreateSummary --> ReturnResponse: JSON Response

    ReturnResponse --> [*]
```

### Chatbot Interaction Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant API as /api/v1/chat/message
    participant GE as Gemini Engine
    participant GM as Gemini AI Model
    participant Session as Session Storage

    C->>API: POST {"message": "Pomidoru nə vaxt suvarmalıyam?", "session_id": "user123"}
    API->>GE: Process message

    GE->>Session: Get or Create Session
    alt Session exists
        Session-->>GE: Return existing chat
    else New session
        Session->>GM: Initialize with system prompt
        GM-->>Session: System context loaded
        Session-->>GE: New chat session
    end

    GE->>GM: Send user message
    Note over GM: Gemini processes with:<br/>- Agricultural context<br/>- Azerbaijani language<br/>- Practical advice focus

    GM-->>GE: AI-generated response
    GE->>GE: Generate quick replies

    Note over GE: Keyword-based:<br/>- "suvar" → Water questions<br/>- "gübrə" → Fertilizer questions<br/>- "xəstə" → Disease questions

    GE-->>API: {"response": "...", "quick_replies": [...]}
    API-->>C: JSON response

    C->>C: Display chat message
    C->>C: Show quick reply buttons
```

## 🔗 Endpoints

### Recommendations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/recommendations` | Ətraflı tövsiyələr al |
| GET | `/api/v1/recommendations/quick` | Sadə parametrlərlə sürətli tövsiyə |

### Farms & Profiles

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/farms` | Ferma tiplərinin siyahısı |
| GET | `/api/v1/farms/{farm_type}/profile` | Ferma profili |
| GET | `/api/v1/scenarios/{farm_type}` | Test ssenariləri |

### Rules

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/rules` | Bütün qaydalar |
| GET | `/api/v1/rules/search?q=keyword` | Qayda axtarışı |
| GET | `/api/v1/rules/{farm_type}` | Ferma tipinə görə qaydalar |
| GET | `/api/v1/rules/{farm_type}/{category}` | Kateqoriyaya görə |

### Constants

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/constants` | Bütün sabitlər |
| GET | `/api/v1/constants/thresholds` | Hədd dəyərləri |
| GET | `/api/v1/constants/regions` | Regionlar |
| GET | `/api/v1/constants/stages` | Mərhələlər |

### Weather Auto-Fetch

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/weather/auto` | İstifadəçinin IP ünvanına əsasən avtomatik hava məlumatı |

**Architecture**: Backend-first approach
- Uses IP geolocation (ipapi.co) to detect user location
- Fetches weather data from Open-Meteo API (free, no API key needed)
- Maps location to Azerbaijan regions (aran, lankaran, sheki_zagatala, etc.)
- Returns temperature, humidity, rainfall, wind speed, and frost warnings

**Benefits**:
- ✅ No API keys exposed to frontend
- ✅ Centralized rate limiting and caching
- ✅ Graceful error handling
- ✅ Regional mapping for Azerbaijan

**Example Response**:
```json
{
  "temperature": 8,
  "humidity": 68,
  "rainfall_last_24h": 0.0,
  "wind_speed": 27,
  "frost_warning": false,
  "location": {
    "city": "Baku",
    "country": "Azerbaijan",
    "region": "Absheron",
    "latitude": 40.4093,
    "longitude": 49.8671
  },
  "region": "aran"
}
```

### Chatbot (Gemini AI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat/message` | Send message to AI chatbot |
| POST | `/api/v1/chat/reset` | Reset chat session |
| GET | `/api/v1/chat/stats` | Get chatbot statistics |
| GET | `/api/v1/chat/examples` | Get example questions |

**Features**:
- ✨ **AI-Powered**: Google Gemini (gemini-flash-latest model)
- 🇦🇿 **Azerbaijani Language**: Native agricultural terminology
- 💬 **Context-Aware**: Session-based conversation history
- ⚡ **Smart Replies**: Contextual quick reply suggestions
- 📊 **Rich Formatting**: Tables, emojis, structured responses
- 🆓 **Free Tier**: No cost for usage

**Example Request**:
```json
POST /api/v1/chat/message
{
  "message": "Pomidoru nə vaxt suvarmalıyam?",
  "session_id": "user123"  // Optional
}
```

**Example Response**:
```json
{
  "response": "💧🍅 Pomidor Suvarma Vaxtı\n\nSalam! Pomidorun suvarma rejimi...",
  "quick_replies": ["💧 Nə qədər su?", "⏰ Nə vaxt suvarım?", "🌊 Hansı üsul?"]
}
```

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Sağlamlıq yoxlaması |
| GET | `/api/v1/stats` | Statistika |

## 📝 Example Usage

### POST /api/v1/recommendations

```json
{
  "farm_type": "wheat",
  "region": "aran",
  "weather": {
    "temperature": 35,
    "humidity": 80,
    "rainfall_last_24h": 0
  },
  "soil": {
    "soil_moisture": 45
  },
  "crop_context": {
    "crop_type": "wheat",
    "stage": "heading",
    "days_since_irrigation": 5,
    "days_since_fertilization": 25
  }
}
```

### Response

```json
{
  "farm_type": "wheat",
  "region": "aran",
  "response_date": "2025-12-26",
  "critical_alerts": [...],
  "high_priority": [...],
  "medium_priority": [...],
  "daily_schedule": [...],
  "total_recommendations": 5,
  "summary_az": "⚠️ DİQQƏT: 2 kritik xəbərdarlıq var!"
}
```

### Quick Recommendation

```
GET /api/v1/recommendations/quick?farm_type=wheat&region=aran&temperature=32&humidity=85&crop_type=wheat&stage=tillering&days_since_irrigation=6&soil_moisture=48
```

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── core/
│   │   └── config.py          # Settings
│   ├── data/
│   │   ├── constants/         # Threshold values
│   │   ├── profiles/          # Farm profiles
│   │   └── rules/             # Rule JSON files
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── services/
│   │   ├── rule_engine.py     # Rule evaluation
│   │   └── rule_loader.py     # JSON loading
│   └── main.py                # FastAPI app
├── requirements.txt
└── run.sh
```

### Data Structure Organization

```mermaid
graph TB
    subgraph "Rule Data Organization"
        Root[app/data/]

        subgraph "Rules by Farm Type"
            Wheat[wheat/]
            Livestock[livestock/]
            Orchard[orchard/]
            Vegetable[vegetable/]
            Mixed[mixed/]
        end

        subgraph "Wheat Rules - 31 rules"
            W1[irrigation.json - 11 rules]
            W2[fertilization.json - 6 rules]
            W3[pest_disease.json - 7 rules]
            W4[harvest.json - 7 rules]
        end

        subgraph "Livestock Rules - 22 rules"
            L1[disease_risk.json - 7 rules]
            L2[feeding.json - 7 rules]
            L3[veterinary.json - 8 rules]
        end

        subgraph "Orchard Rules - 26 rules"
            O1[irrigation.json - 7 rules]
            O2[fertilization.json - 6 rules]
            O3[pruning.json - 6 rules]
            O4[pest_disease.json - 7 rules]
        end

        subgraph "Vegetable Rules - 31 rules"
            V1[irrigation.json - 8 rules]
            V2[fertilization.json - 7 rules]
            V3[greenhouse.json - 8 rules]
            V4[pest_disease.json - 8 rules]
        end

        subgraph "Mixed Rules - 17 rules"
            M1[integration.json - 5 rules]
            M2[resource_allocation.json - 5 rules]
            M3[daily_coordination.json - 7 rules]
        end

        subgraph "Constants"
            C1[thresholds.json]
            C2[regions.json]
            C3[stages.json]
        end

        subgraph "Profiles"
            P1[farm_profiles.json]
        end
    end

    Root --> Wheat
    Root --> Livestock
    Root --> Orchard
    Root --> Vegetable
    Root --> Mixed

    Wheat --> W1
    Wheat --> W2
    Wheat --> W3
    Wheat --> W4

    Livestock --> L1
    Livestock --> L2
    Livestock --> L3

    Orchard --> O1
    Orchard --> O2
    Orchard --> O3
    Orchard --> O4

    Vegetable --> V1
    Vegetable --> V2
    Vegetable --> V3
    Vegetable --> V4

    Mixed --> M1
    Mixed --> M2
    Mixed --> M3

    Root --> C1
    Root --> C2
    Root --> C3
    Root --> P1

    style Wheat fill:#fff59d
    style Livestock fill:#a5d6a7
    style Orchard fill:#ce93d8
    style Vegetable fill:#80cbc4
    style Mixed fill:#ffab91
    style C1 fill:#90caf9
    style C2 fill:#90caf9
    style C3 fill:#90caf9
    style P1 fill:#f48fb1
```

## 📊 Statistics

- **Total Rules**: 127
- **Farm Types**: 5 (wheat, livestock, orchard, vegetable, mixed)
- **Regions**: 5 (aran, lankaran, sheki_zagatala, ganja_gazakh, mountainous)
- **Languages**: Azerbaijani (az) + English (en)

## 🔧 Configuration

### Environment Variables

**REQUIRED**:
- `GEMINI_API_KEY`: Google Gemini AI API key for chatbot
  - Get from: https://aistudio.google.com/app/apikey
  - Free tier available
  - Chatbot will NOT work without this

**Optional**:
- `DEBUG`: Enable debug mode (default: True)
- `CORS_ORIGINS`: Allowed origins for CORS (default: http://localhost:3000)

### Setup

1. Create `.env` file in **project root** (not in backend/ directory):
```bash
cd ..  # Go to project root
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

2. The backend automatically loads `.env` from project root via:
```python
from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)
```

This allows all services (backend + frontend) to share the same `.env` file.

---

*Yonca AI Hackathon - Digital Umbrella Challenge*
