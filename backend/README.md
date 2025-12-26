# Yonca Rule-Based Advisory API

Azərbaycan kənd təsərrüfatı üçün qayda əsaslı məsləhət sistemi.

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

## 📊 Statistics

- **Total Rules**: 127
- **Farm Types**: 5 (wheat, livestock, orchard, vegetable, mixed)
- **Regions**: 5 (aran, lankaran, sheki_zagatala, ganja_gazakh, mountainous)
- **Languages**: Azerbaijani (az) + English (en)

## 🔧 Configuration

Environment variables (optional):
- `DEBUG`: Enable debug mode (default: True)
- `CORS_ORIGINS`: Allowed origins for CORS

---

*Yonca AI Hackathon - Digital Umbrella Challenge*
