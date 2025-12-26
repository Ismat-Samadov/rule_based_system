# Yonca Rule-Based System - Qaydalar Strukturu

## 📁 Fayl Strukturu

```
backend/app/data/
├── constants/                    # Sabit dəyərlər
│   ├── stages.json              # Bitki və heyvan mərhələləri
│   ├── regions.json             # Azərbaycan regionları və iqlim
│   └── thresholds.json          # Hədd dəyərləri (temperatur, rütubət, etc.)
│
├── profiles/                     # Farm profilləri (5 tip)
│   ├── wheat_profile.json       # Taxıl təsərrüfatı
│   ├── livestock_profile.json   # Heyvandarlıq
│   ├── orchard_profile.json     # Meyvə bağı
│   ├── vegetable_profile.json   # Tərəvəzçilik
│   └── mixed_profile.json       # Qarışıq təsərrüfat
│
└── rules/                        # Qaydalar (kateqoriyalara bölünmüş)
    ├── wheat/
    │   ├── irrigation.json      # Suvarma qaydaları (11 qayda)
    │   ├── fertilization.json   # Gübrələmə qaydaları (6 qayda)
    │   ├── pest_disease.json    # Zərərverici/xəstəlik (7 qayda)
    │   └── harvest.json         # Yığım qaydaları (7 qayda)
    │
    ├── livestock/
    │   ├── disease_risk.json    # Xəstəlik riski (7 qayda)
    │   ├── feeding.json         # Yemləmə qaydaları (7 qayda)
    │   └── veterinary.json      # Baytar xidmətləri (8 qayda)
    │
    ├── orchard/
    │   ├── irrigation.json      # Suvarma qaydaları (7 qayda)
    │   ├── fertilization.json   # Gübrələmə qaydaları (6 qayda)
    │   ├── pruning.json         # Budama qaydaları (6 qayda)
    │   └── pest_disease.json    # Zərərverici/xəstəlik (7 qayda)
    │
    ├── vegetable/
    │   ├── irrigation.json      # Suvarma qaydaları (8 qayda)
    │   ├── fertilization.json   # Gübrələmə qaydaları (7 qayda)
    │   ├── greenhouse.json      # Sera idarəetməsi (8 qayda)
    │   └── pest_disease.json    # Zərərverici/xəstəlik (8 qayda)
    │
    └── mixed/
        ├── integration.json     # İnteqrasiya qaydaları (5 qayda)
        ├── resource_allocation.json  # Resurs bölgüsü (5 qayda)
        └── daily_coordination.json   # Gündəlik koordinasiya (7 qayda)
```

## 📊 Statistika

| Kateqoriya | Fayl sayı | Təxmini qayda sayı |
|------------|-----------|-------------------|
| Constants | 3 | - |
| Profiles | 5 | - |
| Wheat Rules | 4 | ~31 |
| Livestock Rules | 3 | ~22 |
| Orchard Rules | 4 | ~26 |
| Vegetable Rules | 4 | ~31 |
| Mixed Rules | 3 | ~17 |
| **CƏMI** | **26** | **~127 qayda** |

## 🔧 Qayda Strukturu

Hər bir qayda aşağıdakı strukturu izləyir:

```json
{
  "rule_id": "WHT_IRR_001",
  "name_az": "Kritik temperatur suvarması",
  "name_en": "Critical temperature irrigation",
  "priority": "critical|high|medium|low|info",
  "enabled": true,
  "conditions": {
    "operator": "AND|OR",
    "items": [
      {"field": "weather.temperature", "operator": ">", "value": 32}
    ]
  },
  "action": {
    "type": "irrigate|fertilize|apply_fungicide|...",
    "urgency": "critical|high|medium|low|info",
    "urgency_score": 0-100
  },
  "message_az": "Azərbaycan dilində mesaj",
  "message_en": "English message"
}
```

## 🏷️ Rule ID Konvensiyası

| Prefix | Farm Tipi |
|--------|-----------|
| WHT_ | Wheat (Buğda) |
| LVS_ | Livestock (Heyvandarlıq) |
| ORCH_ | Orchard (Meyvə bağı) |
| VEG_ | Vegetable (Tərəvəz) |
| MIX_ | Mixed (Qarışıq) |

| Suffix | Kateqoriya |
|--------|------------|
| _IRR_ | Irrigation (Suvarma) |
| _FERT_ | Fertilization (Gübrələmə) |
| _PEST_ | Pest/Disease (Zərərverici/Xəstəlik) |
| _HARV_ | Harvest (Yığım) |
| _DIS_ | Disease Risk (Xəstəlik Riski) |
| _FEED_ | Feeding (Yemləmə) |
| _VET_ | Veterinary (Baytar) |
| _PRUNE_ | Pruning (Budama) |
| _GH_ | Greenhouse (Sera) |
| _INT_ | Integration (İnteqrasiya) |
| _RES_ | Resource (Resurs) |
| _DAY_ | Daily (Gündəlik) |

## 🎯 Urgency Score

| Skor | Səviyyə | Məna |
|------|---------|------|
| 90-100 | Critical | Dərhal müdaxilə lazımdır |
| 70-89 | High | Bu gün həll olunmalı |
| 40-69 | Medium | 1-2 gün ərzində |
| 20-39 | Low | Həftə ərzində |
| 0-19 | Info | Məlumat xarakterli |

## 🌍 Azərbaycan Regionları

- **Aran** - İsti, quru, suvarma asılı
- **Lənkəran** - Subtropik, nəmli
- **Şəki-Zaqatala** - Dağətəyi, mülayim
- **Gəncə-Qazax** - Quru, suvarma asılı
- **Dağlıq** - Soyuq, qısa mövsüm

---

*Yonca AI Hackathon - Digital Umbrella Challenge*
*Rule-Based Agricultural Advisory System*
