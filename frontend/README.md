# Yonca Frontend

Azərbaycan kənd təsərrüfatı üçün qayda əsaslı məsləhət sisteminin Next.js frontend interfeysi.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

Server: http://localhost:3000

## 📁 Struktur

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Landing page
│   ├── globals.css          # Global styles
│   ├── recommendations/
│   │   └── page.tsx         # Recommendations wizard
│   └── farm/
│       └── page.tsx         # Farm profile
├── components/
│   ├── Header.tsx           # Navigation header
│   ├── Footer.tsx           # Footer
│   ├── FarmTypeCard.tsx     # Farm type selector
│   ├── WeatherInput.tsx     # Weather input form
│   ├── RecommendationCard.tsx # Recommendation display
│   └── DailySchedule.tsx    # Daily schedule view
├── lib/
│   └── api.ts               # API client & types
├── tailwind.config.js       # Tailwind configuration
└── package.json
```

## 🎨 Design System

### Rənglər
- **Leaf** (Yaşıl): Primary, success states
- **Earth** (Torpaq): Neutral, backgrounds
- **Wheat** (Sarı): Accent, medium priority
- **Sky** (Mavi): Info, low priority
- **Danger** (Qırmızı): Critical alerts

### Komponentlər
- `.card` - Basic card
- `.card-hover` - Card with hover effect
- `.btn-primary` - Primary button (green)
- `.btn-secondary` - Secondary button (neutral)
- `.btn-danger` - Danger button (red)
- `.input` - Text input
- `.select` - Select dropdown
- `.badge-*` - Status badges (critical, high, medium, low, info)

## 🔗 API Connection

Backend API URL: `http://localhost:8000` (or set `NEXT_PUBLIC_API_URL`)

The Next.js config includes a proxy rewrite to forward `/api/v1/*` requests to the backend.

## 📱 Səhifələr

### Ana Səhifə (`/`)
- Hero section
- Features overview
- Farm types
- CTA

### Tövsiyələr (`/recommendations`)
4 addımlı wizard:
1. Ferma tipi seçimi
2. Hava şəraiti
3. Əlavə detallar
4. Nəticələr

### Ferma Profili (`/farm`)
- Ferma məlumatlarını saxlama
- LocalStorage-də saxlanılır

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Language**: TypeScript

---

*Yonca AI Hackathon - Digital Umbrella Challenge*
