# 🌱 Yonca - Agricultural Advisory System

**Rule-Based AI Recommendation Engine for Azerbaijan Farmers**

Yonca is an intelligent agricultural advisory system designed specifically for Azerbaijan's climate and farming conditions. Built for the Yonca AI Hackathon (Digital Umbrella Challenge), it provides real-time, data-driven recommendations to optimize farm operations.

---

## ✨ Features

- 🎯 **127+ Smart Agricultural Rules** - Comprehensive rule engine covering all major farming scenarios
- 🌾 **5 Farm Type Profiles** - Wheat, Livestock, Orchard, Vegetable, and Mixed farming
- 🌍 **5 Regional Climates** - Adapted for Aran, Lankaran, Sheki-Zagatala, Ganja-Gazakh, and Mountainous regions
- ⚡ **Real-Time Recommendations** - Instant analysis based on weather, soil, and crop conditions
- 📅 **Daily Task Scheduling** - Prioritized action plans with timing recommendations
- 🚨 **Early Warning System** - Critical alerts for pests, diseases, and environmental risks
- 💬 **Intelligent Chatbot** - Natural language interface with 20+ intent types
- 🇦🇿 **Bilingual Support** - Full Azerbaijani and English interfaces

---

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd rule_based_recommendation_system

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access the application:**
- 🌐 Frontend: http://localhost:3000
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

### Manual Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 📊 System Statistics

| Metric | Count |
|--------|-------|
| **Total Rules** | 127 |
| **Farm Types** | 5 |
| **Rule Categories** | 17 |
| **Supported Regions** | 5 |
| **Crop Growth Stages** | 30+ |
| **Chatbot Intents** | 20+ |
| **API Endpoints** | 22 |

---

## 🏗️ Architecture

```
┌─────────────────┐
│  Next.js        │
│  Frontend       │ ← User Interface (3000)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI        │
│  Backend        │ ← API & Rule Engine (8000)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Rule Engine    │
│  + 127 Rules    │ ← Business Logic
│  + JSON Data    │
└─────────────────┘
```

### Technology Stack

**Backend:**
- FastAPI 0.109.0
- Python 3.10+
- Pydantic for validation
- Uvicorn/Gunicorn for serving

**Frontend:**
- Next.js 14.2+ (App Router)
- React 18
- Tailwind CSS 3.3
- Lucide React icons
- Framer Motion for animations

**Deployment:**
- Docker & Docker Compose
- Nginx for reverse proxy
- Let's Encrypt for SSL

---

## 📁 Project Structure

```
rule_based_recommendation_system/
├── backend/
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── chatbot/          # Chatbot engine
│   │   ├── core/             # Configuration
│   │   ├── data/             # Rules & constants
│   │   │   ├── rules/        # 127 agricultural rules
│   │   │   ├── profiles/     # Farm type profiles
│   │   │   └── constants/    # Thresholds & regions
│   │   ├── models/           # Pydantic schemas
│   │   ├── services/         # Rule engine & loader
│   │   └── main.py           # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── validate_json.py      # Data validator
│
├── frontend/
│   ├── app/                  # Next.js pages
│   │   ├── page.tsx          # Landing page
│   │   ├── recommendations/  # Wizard interface
│   │   └── farm/             # Farm profile
│   ├── components/           # Reusable UI components
│   ├── lib/                  # API client & types
│   ├── package.json
│   └── Dockerfile
│
├── docs/                     # Documentation
├── docker-compose.yml        # Orchestration
├── DEPLOYMENT.md             # Deployment guide
└── README.md                 # This file
```

---

## 🌾 Farm Types & Rules

### 1. Wheat/Cereals (31 rules)
- **Categories**: Irrigation (11), Fertilization (6), Pest/Disease (7), Harvest (7)
- **Stages**: Germination → Tillering → Heading → Grain Filling → Maturity
- **Key Alerts**: Heat stress, moisture deficiency, aphid management

### 2. Livestock (22 rules)
- **Categories**: Disease Risk (7), Feeding (7), Veterinary (8)
- **Animals**: Cattle, Sheep, Goat, Poultry
- **Key Alerts**: Heat stress, ventilation, vaccination schedules

### 3. Orchard (26 rules)
- **Categories**: Irrigation (7), Fertilization (6), Pruning (6), Pest/Disease (7)
- **Crops**: Grape, Pomegranate, Apple, Fig
- **Key Alerts**: Frost protection, fungal diseases, irrigation timing

### 4. Vegetable (31 rules)
- **Categories**: Irrigation (8), Fertilization (7), Greenhouse (8), Pest/Disease (8)
- **Crops**: Tomato, Cucumber, Potato, Pepper
- **Key Alerts**: Greenhouse climate, calcium deficiency, blight management

### 5. Mixed Farming (17 rules)
- **Categories**: Integration (5), Resource Allocation (5), Daily Coordination (7)
- **Focus**: Optimal resource sharing between crops and livestock

---

## 🔧 API Endpoints

### Recommendations
- `POST /api/v1/recommendations` - Get personalized farming recommendations
- `GET /api/v1/recommendations/quick` - Quick recommendation with minimal parameters

### Farms & Profiles
- `GET /api/v1/farms` - List all farm types
- `GET /api/v1/farms/{farm_type}/profile` - Get detailed farm profile
- `GET /api/v1/scenarios/{farm_type}` - Get test scenarios

### Rules
- `GET /api/v1/rules` - List all rules
- `GET /api/v1/rules/search?q=keyword` - Search rules
- `GET /api/v1/rules/{farm_type}` - Rules for specific farm type
- `GET /api/v1/rules/{farm_type}/{category}` - Category-specific rules

### Chatbot
- `POST /api/v1/chat/message` - Send message to chatbot
- `GET /api/v1/chat/intents` - List available intents
- `GET /api/v1/chat/examples` - Get example questions

### Constants
- `GET /api/v1/constants` - Get all constants (regions, stages, thresholds)
- `GET /api/v1/constants/thresholds` - Temperature/moisture limits
- `GET /api/v1/constants/regions` - Azerbaijan region data

---

## 📖 Usage Examples

### Get Wheat Recommendations

```bash
curl -X POST http://localhost:8000/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

### Chat with Bot

```bash
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Buğdanı nə vaxt suvarmalıyam?",
    "session_id": "user123"
  }'
```

---

## 🌍 Regional Support

| Region | Climate Type | Key Characteristics |
|--------|-------------|-------------------|
| **Aran** | Semi-arid | Hot, dry, irrigation-dependent |
| **Lankaran** | Subtropical | Humid, high rainfall, rice/tea suitable |
| **Sheki-Zagatala** | Temperate | Moderate, fruit orchards, hazelnut |
| **Ganja-Gazakh** | Dry continental | Dry, wheat & grapes, irrigation needed |
| **Mountainous** | Alpine | Cold, short growing season, potatoes |

---

## 🧪 Testing & Validation

### Validate JSON Data

```bash
cd backend
python validate_json.py
```

**Output:**
```
✅ All 26 JSON files valid
✅ 127 rules validated
✅ No structure errors
```

### Run Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Test Frontend Build

```bash
cd frontend
npm run build
npm run lint
```

---

## 🐳 Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy:**
```bash
docker-compose up -d
```

**Production Deploy:**
- Configure environment variables
- Set up Nginx reverse proxy
- Enable SSL with Let's Encrypt
- Configure firewall rules
- Set up monitoring

---

## 🔐 Security

- ✅ Input validation with Pydantic
- ✅ CORS configuration
- ✅ Health check endpoints
- ✅ Non-root Docker users
- ⏳ Rate limiting (TODO)
- ⏳ Authentication & authorization (TODO)

---

## 📈 Future Enhancements

- [ ] User authentication & profiles
- [ ] PostgreSQL database for persistence
- [ ] Redis caching layer
- [ ] Mobile app (React Native)
- [ ] Weather API integration
- [ ] IoT sensor support
- [ ] Advanced analytics dashboard
- [ ] Multi-language i18n framework
- [ ] Machine learning predictions
- [ ] Export recommendations as PDF

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📄 License

This project was developed for the Yonca AI Hackathon - Digital Umbrella Challenge.

---

## 👥 Team

Built with ❤️ for Azerbaijan farmers

---

## 📞 Support

- 📖 **Documentation**: See `/docs` folder
- 🐛 **Issues**: GitHub Issues
- 💬 **Discussions**: GitHub Discussions
- 📧 **Email**: support@yonca.az (placeholder)

---

**Version:** 1.0.0
**Last Updated:** December 27, 2025
**Status:** ✅ Production Ready
