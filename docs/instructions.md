# Rule-Based Farm Advisory System - Tam Təlimat

## 📋 Layihə Strukturu

```
yonca-rule-based-system/
│
├── docs/
│   └── RULES_SPECIFICATION.md      # Bu sənəd
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── config.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── farm_models.py      # Pydantic models
│   │   │   └── response_models.py
│   │   ├── rules/
│   │   │   ├── __init__.py
│   │   │   ├── base_engine.py      # Core rule engine
│   │   │   ├── irrigation.py
│   │   │   ├── fertilization.py
│   │   │   ├── pest_management.py
│   │   │   ├── harvest.py
│   │   │   └── livestock.py
│   │   ├── data/
│   │   │   ├── wheat_rules.json
│   │   │   ├── livestock_rules.json
│   │   │   ├── orchard_rules.json
│   │   │   ├── vegetable_rules.json
│   │   │   └── mixed_rules.json
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── recommendations.py
│   │   │   ├── farms.py
│   │   │   └── schedule.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── recommendation_service.py
│   │       └── schedule_generator.py
│   ├── tests/
│   │   └── test_rules.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx
│   │   │   ├── layout.tsx
│   │   │   ├── farms/
│   │   │   │   └── [type]/
│   │   │   │       └── page.tsx
│   │   │   └── api/
│   │   │       └── recommendations/
│   │   │           └── route.ts
│   │   ├── components/
│   │   │   ├── FarmSelector.tsx
│   │   │   ├── RecommendationCard.tsx
│   │   │   ├── DailySchedule.tsx
│   │   │   ├── WeatherInput.tsx
│   │   │   └── AlertBanner.tsx
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   └── types.ts
│   │   └── styles/
│   │       └── globals.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── next.config.js
│
└── README.md
```

---

# 📖 BÖLMƏ 1: QAYDALAR SPESİFİKASİYASI

## 1.1 Challenge Tələblərindən Çıxarılan Əsas Prinsiplər

Sənədlərdən (Challenge Brief) çıxarılan tələblər:

| Tələb                                                                                   | Mənbə                 | İmplementasiya                |
| ----------------------------------------------------------------------------------------- | ----------------------- | ------------------------------ |
| "Daily farm operations üçün AI-driven recommendation engine"                           | Challenge Brief, səh.2 | Gündəlik tövsiyə sistemi   |
| "Irrigation, fertilization, pest/disease risklərinə dair scenario-based advisory logic" | Challenge Brief, səh.2 | Üç əsas qayda kategoriyası |
| "Minimum 5 fərqli təsərrüfat ssenarisi üzrə stabil işləyən prototip"             | Challenge Brief, səh.2 | 5 farm profili                 |
| "Recommendation strukturunun ≥ 90% logical accuracy"                                     | Challenge Brief, səh.2 | Deterministik qaydalar         |
| "Fermer rutininin avtomatik schedule-ının generasiyası"                                | Challenge Brief, səh.2 | Schedule generator             |
| "100% data-safety — heç bir mərhələdə real data istifadə edilmir"                  | Challenge Brief, səh.2 | Yalnız synthetic/dummy data   |
| "Azərbaycan dilində çalışan"                                                         | Challenge Brief, səh.2 | AZ dil dəstəyi               |

---

## 1.2 Beş Farm Profili Tərifləri

Challenge Brief-dən: *"5 və ya daha çox müxtəlif farm profile (planting, livestock, mixed, orchard və s.)"*

### Profil 1: TAXIL TƏSƏRRÜFATİ (Wheat/Grain Production)

### Profil 2: HEYVANDARLİQ (Livestock)

### Profil 3: MEYVƏ BAĞI (Orchard)

### Profil 4: TƏRƏVƏZ TƏSƏRRÜFATİ (Vegetable)

### Profil 5: QARİŞİQ TƏSƏRRÜFAT (Mixed Farming)

---

# 📖 BÖLMƏ 2: TAXIL TƏSƏRRÜFATİ (WHEAT) QAYDALARI

## 2.1 Məhsul Mərhələləri (Growth Stages)

```
STAGE_ID | Stage Name (EN)    | Stage Name (AZ)      | Gün Aralığı | Kritik Faktorlar
---------|--------------------|-----------------------|-------------|------------------
WHT_S1   | Germination        | Cücərmə               | 0-10        | Torpaq nəmliyi, temperatur
WHT_S2   | Tillering          | Kollanma              | 11-40       | Azot, su
WHT_S3   | Stem Extension     | Gövdə uzanması        | 41-60       | Su, temperatur
WHT_S4   | Heading            | Sünbülləmə            | 61-80       | Su stressi kritik
WHT_S5   | Grain Filling      | Dən dolması           | 81-105      | Temperatur, su
WHT_S6   | Maturity           | Yetişmə               | 106-120     | Quru şərait
```

## 2.2 Suvarma Qaydaları (Irrigation Rules)

### Qayda WHT_IRR_001: Kritik Temperatur Suvarması

```yaml
rule_id: WHT_IRR_001
name_az: "Kritik temperatur suvarması"
name_en: "Critical temperature irrigation"
priority: CRITICAL
conditions:
  - temperature > 32°C
  - stage IN [WHT_S2, WHT_S3, WHT_S4, WHT_S5]
  - last_irrigation_hours > 24
action:
  type: IRRIGATE
  urgency: CRITICAL
  timing: "Səhər 05:00-07:00 və ya axşam 19:00-21:00"
  amount_mm_per_ha: 30-35
  method: "Damcı və ya yağmurlama"
message_az: "TƏCILI: Temperatur {temperature}°C - buğda üçün kritik həddədir. Dərhal suvarma tələb olunur."
message_en: "URGENT: Temperature {temperature}°C is critical for wheat. Immediate irrigation required."
reasoning: "32°C-dən yuxarı temperaturda buğda bitkisi istilik stressinə məruz qalır, bu da məhsuldarlığı 20-40% azalda bilər."
```

### Qayda WHT_IRR_002: Torpaq Nəmliyi Əsaslı Suvarma

```yaml
rule_id: WHT_IRR_002
name_az: "Torpaq nəmliyi əsaslı suvarma"
name_en: "Soil moisture based irrigation"
priority: HIGH
conditions:
  stage: WHT_S1 (Cücərmə)
    - soil_moisture < 60% → IRRIGATE
  stage: WHT_S2 (Kollanma)
    - soil_moisture < 50% → IRRIGATE
  stage: WHT_S3 (Gövdə uzanması)
    - soil_moisture < 55% → IRRIGATE
  stage: WHT_S4 (Sünbülləmə)
    - soil_moisture < 55% → IRRIGATE (CRITICAL - bu mərhələdə su stressi məhsulu 30% azaldır)
  stage: WHT_S5 (Dən dolması)
    - soil_moisture < 45% → IRRIGATE
  stage: WHT_S6 (Yetişmə)
    - soil_moisture < 35% → IRRIGATE (minimal)
action:
  type: IRRIGATE
  timing: "Səhər erkən və ya axşam"
  amount_calculation: |
    base_amount = 25 mm/ha
    if temperature > 30: base_amount += 5
    if humidity < 40: base_amount += 5
    if rainfall_last_7_days > 10: base_amount -= rainfall_last_7_days * 0.7
    final_amount = max(0, base_amount)
message_az: "Torpaq nəmliyi {soil_moisture}% - {stage} mərhələsi üçün minimum {threshold}% olmalıdır. Suvarma tövsiyə olunur."
```

### Qayda WHT_IRR_003: Suvarma İntervalı

```yaml
rule_id: WHT_IRR_003
name_az: "Müntəzəm suvarma intervalı"
name_en: "Regular irrigation interval"
priority: MEDIUM
conditions:
  stage: WHT_S1 → max_interval: 3 gün
  stage: WHT_S2 → max_interval: 5 gün
  stage: WHT_S3 → max_interval: 4 gün
  stage: WHT_S4 → max_interval: 4 gün
  stage: WHT_S5 → max_interval: 6 gün
  stage: WHT_S6 → max_interval: 10 gün (və ya heç - yetişmə dövrü)
  
  IF days_since_irrigation >= max_interval:
    action: IRRIGATE
exception:
  - IF rainfall_last_7_days > 15mm: interval += 2 gün
  - IF humidity > 75%: interval += 1 gün
message_az: "Son suvarmadan {days} gün keçib. {stage} mərhələsində hər {interval} gündən bir suvarma tövsiyə olunur."
```

### Qayda WHT_IRR_004: Yağış Kompensasiyası

```yaml
rule_id: WHT_IRR_004
name_az: "Yağış sonrası suvarma tənzimləməsi"
name_en: "Post-rainfall irrigation adjustment"
priority: INFO
conditions:
  - rainfall_last_24h > 0
action:
  calculation: |
    IF rainfall_last_24h >= 20mm:
      skip_irrigation = True
      next_irrigation_delay = 3 gün
    ELIF rainfall_last_24h >= 10mm:
      reduce_amount_by = 50%
      next_irrigation_delay = 2 gün
    ELIF rainfall_last_24h >= 5mm:
      reduce_amount_by = 25%
message_az: "Son 24 saatda {rainfall}mm yağış olub. Suvarma {action}."
```

## 2.3 Gübrələmə Qaydaları (Fertilization Rules)

### Qayda WHT_FERT_001: Əkin Öncəsi Gübrələmə

```yaml
rule_id: WHT_FERT_001
name_az: "Əkin öncəsi əsas gübrələmə"
name_en: "Pre-planting base fertilization"
priority: HIGH
conditions:
  - stage == PRE_PLANTING (əkindən 7-10 gün əvvəl)
  - last_fertilization IS NULL OR days_since > 180
action:
  type: FERTILIZE
  fertilizer_type: "NPK 15-15-15"
  amount_kg_per_ha: 200-250
  method: "Torpağa qarışdırmaqla"
  timing: "Əkindən 7-10 gün əvvəl"
message_az: "Əkin öncəsi gübrələmə vaxtıdır. NPK 15-15-15 gübrəsindən hektara 200-250 kq tövsiyə olunur."
```

### Qayda WHT_FERT_002: Kollanma Dövrü Azot Gübrəsi

```yaml
rule_id: WHT_FERT_002
name_az: "Kollanma dövrü azot gübrəsi"
name_en: "Tillering stage nitrogen application"
priority: HIGH
conditions:
  - stage == WHT_S2 (Kollanma)
  - days_in_stage >= 10
  - days_since_fertilization > 20 OR nitrogen_applied_this_stage == False
action:
  type: FERTILIZE
  fertilizer_type: "Ammonium Nitrat (NH4NO3) və ya Karbamid"
  amount_kg_per_ha: 
    ammonium_nitrate: 150-200
    urea: 100-130
  timing: "Kollanma başlayandan 10-15 gün sonra"
  method: "Səpələmə, suvarma öncəsi"
message_az: "Kollanma dövrü azot gübrələməsi vaxtıdır. Gövdə sayını artırmaq üçün kritikdir."
reasoning: "Kollanma mərhələsində azot çatışmazlığı gövdə sayını və nəticədə məhsuldarlığı ciddi azaldır."
```

### Qayda WHT_FERT_003: Sünbülləmə Öncəsi Gübrələmə

```yaml
rule_id: WHT_FERT_003
name_az: "Sünbülləmə öncəsi gübrələmə"
name_en: "Pre-heading fertilization"
priority: MEDIUM
conditions:
  - stage == WHT_S3 (Gövdə uzanması, sünbülləməyə yaxın)
  - days_until_heading <= 10 (təxmini)
action:
  type: FERTILIZE
  fertilizer_type: "Karbamid + Mikroelementlər (Sink, Bor)"
  amount_kg_per_ha:
    urea: 50-70
    zinc_sulfate: 5-10
  method: "Yarpaq gübrələməsi (foliar) və ya torpağa"
message_az: "Sünbülləmə öncəsi son gübrələmə. Dən keyfiyyəti üçün vacibdir."
```

### Qayda WHT_FERT_004: Gübrələmə Qadağası

```yaml
rule_id: WHT_FERT_004
name_az: "Gübrələmə dayandırma qaydası"
name_en: "Fertilization stop rule"
priority: INFO
conditions:
  - stage IN [WHT_S5, WHT_S6] (Dən dolması, Yetişmə)
action:
  type: NO_FERTILIZATION
message_az: "Bu mərhələdə gübrələmə tövsiyə olunmur. Dən dolması və yetişmə dövründə əlavə gübrə keyfiyyəti aşağı sala bilər."
```

## 2.4 Zərərverici və Xəstəlik Qaydaları (Pest & Disease Rules)

### Qayda WHT_PEST_001: Pas Xəstəliyi Riski

```yaml
rule_id: WHT_PEST_001
name_az: "Pas xəstəliyi riski"
name_en: "Rust disease risk"
priority: HIGH
conditions:
  - temperature BETWEEN 15°C AND 25°C
  - humidity > 70%
  - stage IN [WHT_S2, WHT_S3, WHT_S4]
  - consecutive_humid_days >= 3
risk_level_calculation: |
  risk = 0
  IF humidity > 80%: risk += 2
  ELIF humidity > 70%: risk += 1
  IF temperature BETWEEN 18 AND 22: risk += 2  # optimal for rust
  IF consecutive_humid_days > 5: risk += 1
  
  IF risk >= 4: level = "HIGH"
  ELIF risk >= 2: level = "MEDIUM"
  ELSE: level = "LOW"
action:
  IF level == "HIGH":
    type: APPLY_FUNGICIDE
    urgency: HIGH
    product: "Propiconazole və ya Tebuconazole əsaslı fungisid"
    timing: "Dərhal, səhər şeh quruduqdan sonra"
  IF level == "MEDIUM":
    type: MONITOR
    urgency: MEDIUM
    message: "Yarpaqlarda sarı-narıncı ləkələr yoxlayın"
message_az: "Pas xəstəliyi riski {level}. Temperatur {temp}°C və rütubət {humidity}% - pas üçün əlverişli şərait."
```

### Qayda WHT_PEST_002: Mənənə (Aphid) Riski

```yaml
rule_id: WHT_PEST_002
name_az: "Mənənə hücumu riski"
name_en: "Aphid infestation risk"
priority: MEDIUM
conditions:
  - temperature > 20°C
  - humidity BETWEEN 40% AND 70%
  - stage IN [WHT_S3, WHT_S4, WHT_S5]
  - wind_speed < 15 km/h
risk_level_calculation: |
  risk = 0
  IF temperature BETWEEN 25 AND 30: risk += 2  # optimal for aphids
  IF humidity BETWEEN 50 AND 65: risk += 1
  IF stage == WHT_S4: risk += 1  # most vulnerable at heading
  IF wind_speed < 10: risk += 1  # calm weather favors aphids
  
  IF risk >= 4: level = "HIGH"
  ELIF risk >= 2: level = "MEDIUM"
  ELSE: level = "LOW"
action:
  IF level == "HIGH":
    type: APPLY_INSECTICIDE
    product: "İmidakloprid və ya Tiametoksam"
    timing: "Səhər tezdən və ya axşam"
    note: "Arılar üçün təhlükəli - çiçəklənmə vaxtı istifadə etməyin"
  IF level == "MEDIUM":
    type: MONITOR
    frequency: "Hər 2 gündən bir yoxlama"
message_az: "Mənənə riski {level}. Sünbül və yarpaqlarda yoxlama aparın."
```

### Qayda WHT_PEST_003: Sürmə Xəstəliyi

```yaml
rule_id: WHT_PEST_003
name_az: "Sürmə xəstəliyi riski"
name_en: "Smut disease risk"
priority: MEDIUM
conditions:
  - stage == WHT_S1 (Cücərmə)
  - seed_treatment == False OR seed_treatment == UNKNOWN
  - soil_moisture > 70%
action:
  type: PREVENTIVE_ALERT
  message_az: "Toxum dərmanlanmayıbsa, sürmə xəstəliyi riski var. Növbəti mövsüm üçün toxum dərmanlamasını unutmayın."
  recommendation: "Karboksil və ya Tiram əsaslı toxum dərmanı"
```

## 2.5 Məhsul Yığımı Qaydaları (Harvest Rules)

### Qayda WHT_HARV_001: Yığım Hazırlığı

```yaml
rule_id: WHT_HARV_001
name_az: "Yığım hazırlığı göstəricisi"
name_en: "Harvest readiness indicator"
priority: INFO
conditions:
  - stage == WHT_S6 (Yetişmə)
  - days_in_stage >= 10
  - grain_moisture <= 14% (ideal)
  - grain_color == "golden" (saman sarısı)
indicators:
  ready_to_harvest:
    - Dən rütubəti 13-14%
    - Sünbül tamamilə saralmış
    - Dən bərk, dırnaqla çətinliklə sınır
    - Saman quru və kövrək
  too_early:
    - Dən rütubəti > 16%
    - Sünbüldə yaşıl hissələr var
    - Dən yumşaq
  too_late:
    - Dən tökülməyə başlayıb
    - Sünbüllər əyilib
action:
  IF ready_to_harvest:
    type: HARVEST
    urgency: HIGH
    timing: "Növbəti 3-5 gün ərzində, quru havada"
    note: "Yağışdan əvvəl yığmağa çalışın"
  IF too_late:
    type: URGENT_HARVEST
    urgency: CRITICAL
    message: "Dən tökülməsi başlayıb, dərhal yığım!"
message_az: "Buğda yığıma hazırdır. Dən rütubəti {moisture}%, ideal şərait."
```

### Qayda WHT_HARV_002: Hava Şəraiti Yığım Qərarı

```yaml
rule_id: WHT_HARV_002
name_az: "Hava şəraitinə görə yığım qərarı"
name_en: "Weather-based harvest decision"
priority: HIGH
conditions:
  - stage == WHT_S6
  - harvest_ready == True
weather_rules:
  ideal:
    - temperature: 25-35°C
    - humidity: < 60%
    - rainfall_forecast_48h: 0mm
    - wind_speed: < 20 km/h
    action: "Yığıma başlayın"
  acceptable:
    - temperature: 20-38°C
    - humidity: 60-75%
    - rainfall_forecast_48h: 0mm
    action: "Yığım mümkündür, günün isti saatlarında"
  postpone:
    - humidity: > 75%
    - OR rainfall_forecast_48h: > 0mm
    - OR morning_dew: heavy
    action: "Yığımı təxirə salın, şeh quruyana qədər gözləyin"
  urgent:
    - rainfall_forecast_48h: > 10mm
    - AND harvest_ready: True
    action: "TƏCILI yığım - yağışdan əvvəl mümkün qədər sahəni biçin"
message_az: "Hava şəraiti: {condition}. Yığım tövsiyəsi: {action}."
```

---

# 📖 BÖLMƏ 3: HEYVANDARLİQ (LIVESTOCK) QAYDALARI

## 3.1 Heyvan Kateqoriyaları

```
ANIMAL_ID | Heyvan (AZ)      | Animal (EN)    | Alt kateqoriyalar
----------|------------------|----------------|-------------------
LVS_CTL   | İribuynuzlu      | Cattle         | Süd inəyi, Ət istehsalı, Dana
LVS_SHP   | Qoyun            | Sheep          | Ət, Yun, Südlük
LVS_GOT   | Keçi             | Goat           | Süd, Ət
LVS_PLT   | Quşçuluq         | Poultry        | Toyuq, Ördək, Hind toyuğu
```

## 3.2 Xəstəlik Riski Qaydaları

### Qayda LVS_DIS_001: İribuynuzlu - Mastit Riski

```yaml
rule_id: LVS_DIS_001
name_az: "Mastit xəstəliyi riski"
name_en: "Mastitis risk for cattle"
priority: HIGH
animal_type: LVS_CTL
applicable_to: ["dairy_cow"]
conditions:
  - humidity > 75%
  - barn_hygiene_score < 6 (1-10 şkalası)
  - milking_equipment_clean == False OR UNKNOWN
  - temperature > 25°C (istilik stressi)
risk_factors:
  high_risk:
    - humidity > 85% AND temperature > 28°C
    - barn_hygiene_score < 4
    - visible_udder_injury == True
    - milk_appearance_abnormal == True
  medium_risk:
    - humidity > 75%
    - barn_hygiene_score BETWEEN 4 AND 6
    - days_since_vet_check > 30
action:
  IF high_risk:
    type: VETERINARY_ALERT
    urgency: CRITICAL
    message_az: "Mastit riski ÇOX YÜKSƏK. Dərhal baytar çağırın. Xəstə heyvanları ayırın."
    immediate_actions:
      - "Yelin təmizliyini yoxlayın"
      - "Südü laboratoriyaya göndərin"
      - "Sağım avadanlığını dezinfeksiya edin"
  IF medium_risk:
    type: PREVENTIVE_ACTION
    urgency: HIGH
    message_az: "Mastit riski var. Gigiyena tədbirləri gücləndirilməlidir."
    actions:
      - "Tövlə təmizliyini artırın"
      - "Sağım öncəsi/sonrası yelin dezinfeksiyası"
      - "Döşəmə qurulunu təmin edin"
```

### Qayda LVS_DIS_002: Qoyun - Parazit Riski

```yaml
rule_id: LVS_DIS_002
name_az: "Daxili parazit riski"
name_en: "Internal parasite risk for sheep"
priority: HIGH
animal_type: LVS_SHP
conditions:
  - season IN ["spring", "summer", "early_autumn"]
  - pasture_used == True
  - days_since_deworming > 60
  - rainfall_last_month > average
  - temperature > 15°C
risk_indicators:
  clinical_signs:
    - "Zəif bədən kondisiyası"
    - "Solğun göz selikli qişası (FAMACHA skoru yüksək)"
    - "İshal"
    - "Yun tökülməsi"
    - "Arıqlama"
risk_level_calculation: |
  risk = 0
  IF days_since_deworming > 90: risk += 2
  IF season == "spring": risk += 2
  IF rainfall_last_month > 50mm: risk += 1
  IF pasture_density > 10_sheep_per_hectare: risk += 1
  IF any(clinical_signs): risk += 2
  
  IF risk >= 5: level = "HIGH"
  ELIF risk >= 3: level = "MEDIUM"
  ELSE: level = "LOW"
action:
  IF level == "HIGH":
    type: DEWORMING
    urgency: HIGH
    product: "Albendazol və ya İvermektin"
    note: "Baytar məsləhəti tövsiyə olunur, dozanı bədən çəkisinə görə hesablayın"
  IF level == "MEDIUM":
    type: FECAL_TEST
    message_az: "Nəcis analizini tövsiyə edirik. FAMACHA skorunu yoxlayın."
  routine:
    - "Otlaqları növbə ilə istifadə edin"
    - "Nəm ərazilərdən uzaq otlaq seçin"
message_az: "Parazit riski {level}. Son dərmanlamadan {days} gün keçib."
```

### Qayda LVS_DIS_003: Quşçuluq - Respirator Xəstəlik Riski

```yaml
rule_id: LVS_DIS_003
name_az: "Respirator xəstəlik riski"
name_en: "Respiratory disease risk for poultry"
priority: CRITICAL
animal_type: LVS_PLT
conditions:
  - ammonia_level > 25ppm (hiss edilən qoxu)
  - ventilation == "poor"
  - humidity > 70%
  - temperature_fluctuation > 10°C (gün ərzində)
  - bird_density > recommended
warning_signs:
  - "Asqırma, öskürək səsləri"
  - "Gözlərdə sulanma"
  - "Burun axıntısı"
  - "Tüklərin pırtlaşması"
  - "Yem istehlahının azalması"
  - "Yumurta istehsalının düşməsi"
risk_calculation: |
  risk = 0
  IF ventilation == "poor": risk += 3
  IF humidity > 80%: risk += 2
  IF ammonia_level > 25ppm: risk += 2
  IF temperature_fluctuation > 15°C: risk += 2
  IF any(warning_signs): risk += 3
  
  IF risk >= 6: level = "CRITICAL"
  ELIF risk >= 4: level = "HIGH"
  ELIF risk >= 2: level = "MEDIUM"
  ELSE: level = "LOW"
action:
  IF level == "CRITICAL":
    type: EMERGENCY_VET
    urgency: CRITICAL
    message_az: "TƏCILI: Respirator xəstəlik əlamətləri. Quşları izolə edin, baytar çağırın."
    immediate:
      - "Ventilyasiyanı dərhal yaxşılaşdırın"
      - "Xəstə quşları ayırın"
      - "Biosecurity tədbirlərini gücləndirin"
  IF level == "HIGH":
    type: PREVENTIVE
    urgency: HIGH
    actions:
      - "Ventilyasiyanı artırın"
      - "Döşəməni dəyişin"
      - "Ammiak səviyyəsini azaldın"
      - "Temperatur stabilliyini təmin edin"
message_az: "Respirator xəstəlik riski {level}. Ventilyasiya: {ventilation}, Rütubət: {humidity}%"
```

## 3.3 Yemləmə Qaydaları

### Qayda LVS_FEED_001: İstilik Stressi Yemləmə Tənzimləməsi

```yaml
rule_id: LVS_FEED_001
name_az: "İstilik stressi zamanı yemləmə"
name_en: "Heat stress feeding adjustment"
priority: HIGH
applicable_to: [LVS_CTL, LVS_SHP, LVS_GOT, LVS_PLT]
conditions:
  - temperature > 30°C
  - OR temperature > 28°C AND humidity > 70%
  - OR THI (Temperature-Humidity Index) > 72
THI_calculation: |
  THI = (1.8 × T + 32) − (0.55 − 0.0055 × RH) × (1.8 × T − 26)
  where T = temperature (°C), RH = relative humidity (%)
action:
  cattle:
    - "Yemi 20% azaldın, keyfiyyəti artırın"
    - "Səhər və axşam yemlənməsinə keçin (soyuq saatlar)"
    - "Su girişini 50% artırın"
    - "Kölgəlik/sovutma təmin edin"
    - "Mineral əlavələr (Na, K) artırın"
  sheep_goat:
    - "Günorta otlatmanı dayandırın"
    - "Səhər erkən və axşam geç otladın"
    - "Su məntəqələrinin sayını artırın"
  poultry:
    - "Yem istehlahı düşəcək - normaldır"
    - "Elektrolit əlavəsi verin"
    - "Səhər erkən yemlənmə"
    - "Su temperaturunu soyuq saxlayın"
message_az: "İstilik stressi şəraiti. THI={thi}. Yemləmə rejimini dəyişin."
```

### Qayda LVS_FEED_002: Soyuq Hava Yemləmə Tənzimləməsi

```yaml
rule_id: LVS_FEED_002
name_az: "Soyuq hava yemləmə tənzimləməsi"
name_en: "Cold weather feeding adjustment"
priority: MEDIUM
applicable_to: [LVS_CTL, LVS_SHP, LVS_GOT]
conditions:
  - temperature < 5°C
  - OR temperature < 10°C AND wind_speed > 20 km/h (wind chill)
action:
  cattle:
    - "Yemi 10-20% artırın"
    - "Enerji tərkibli yemlər əlavə edin (arpa, qarğıdalı)"
    - "Ilıq su təmin edin (donmuş su içmirlər)"
  sheep_goat:
    - "Ot rasionunu 15% artırın"
    - "Konsentrat əlavə edin"
    - "Sığınacaq təmin edin"
message_az: "Soyuq hava şəraiti. Yem normasını artırın, ilıq su təmin edin."
```

## 3.4 Peyvənd və Baytar Yoxlaması Qaydaları

### Qayda LVS_VET_001: Peyvənd Təqvimi Xatırlatması

```yaml
rule_id: LVS_VET_001
name_az: "Peyvənd vaxtı xatırlatması"
name_en: "Vaccination schedule reminder"
priority: HIGH
vaccination_schedules:
  cattle:
    - name: "Şap xəstəliyi (FMD)"
      frequency: "6 ayda bir"
      alert_days_before: 14
    - name: "Brusellyoz"
      frequency: "İllik"
      alert_days_before: 30
    - name: "Qarayara (Anthrax)"
      frequency: "İllik, yaz"
      alert_days_before: 30
  sheep:
    - name: "Enterotoksemiya (Clostridial)"
      frequency: "İllik, quzulamadan əvvəl"
      alert_days_before: 21
    - name: "Bradzot"
      frequency: "İllik"
      alert_days_before: 30
  poultry:
    - name: "Newcastle"
      frequency: "Yaş proqramına görə"
      ages: [7, 21, 35 gün, sonra 3 ayda bir]
    - name: "Gumboro (IBD)"
      frequency: "14 və 24 günlükdə"
    - name: "Marek"
      frequency: "1 günlükdə (çıxışda)"
action:
  IF days_until_vaccination <= alert_days_before:
    type: VACCINATION_REMINDER
    urgency: HIGH
    message_az: "{vaccine_name} peyvəndinə {days} gün qalıb. Baytar ilə əlaqə saxlayın."
```

### Qayda LVS_VET_002: Müntəzəm Baytar Yoxlaması

```yaml
rule_id: LVS_VET_002
name_az: "Müntəzəm baytar yoxlaması"
name_en: "Routine veterinary checkup"
priority: MEDIUM
conditions:
  - days_since_vet_check > 30 (dairy cattle)
  - days_since_vet_check > 60 (beef cattle, sheep, goat)
  - days_since_vet_check > 90 (poultry flock)
action:
  type: VET_CHECKUP_REMINDER
  urgency: MEDIUM
  message_az: "Son baytar yoxlamasından {days} gün keçib. Müntəzəm yoxlama tövsiyə olunur."
  checklist:
    cattle:
      - "Bədən kondisiyası"
      - "Ayaq/dırnaq vəziyyəti"
      - "Yelin sağlamlığı (süd inəkləri)"
      - "Reproduktiv yoxlama"
    sheep_goat:
      - "FAMACHA skoru"
      - "Bədən kondisiyası"
      - "Ayaq vəziyyəti"
      - "Dişlər"
    poultry:
      - "Ümumi sürü sağlamlığı"
      - "Tələfat dərəcəsi"
      - "Yumurta istehsalı"
```

---

# 📖 BÖLMƏ 4: MEYVƏ BAĞI (ORCHARD) QAYDALARI

## 4.1 Meyvə Növləri və Mərhələləri

```
ORCH_ID   | Meyvə (AZ)    | Fruit (EN) | Mərhələlər
----------|---------------|------------|----------------------------------
ORCH_APL  | Alma          | Apple      | Qış yuxusu, Tumurcuqlanma, Çiçəkləmə, Meyvə əmələ gəlməsi, Yetişmə
ORCH_GRP  | Üzüm          | Grape      | Qış yuxusu, Tumurcuqlanma, Çiçəkləmə, Gilə böyüməsi, Veraison, Yetişmə
ORCH_NAR  | Nar           | Pomegranate| Qış yuxusu, Tumurcuqlanma, Çiçəkləmə, Meyvə inkişafı, Yetişmə
ORCH_FIG  | Əncir         | Fig        | Qış yuxusu, Tumurcuqlanma, Meyvə inkişafı, Yetişmə
ORCH_PST  | Fındıq/Püstə  | Nut        | Qış yuxusu, Tumurcuqlanma, Çiçəkləmə, Qabıq bərkiməsi, Yetişmə
```

## 4.2 Suvarma Qaydaları

### Qayda ORCH_IRR_001: Çiçəkləmə Dövrü Suvarma

```yaml
rule_id: ORCH_IRR_001
name_az: "Çiçəkləmə dövrü suvarma"
name_en: "Flowering period irrigation"
priority: CRITICAL
applicable_to: [ORCH_APL, ORCH_GRP, ORCH_NAR]
conditions:
  - stage == "flowering"
  - soil_moisture < 50%
action:
  type: IRRIGATE
  urgency: HIGH
  amount: "Damcı suvarma - normal normanın 70-80%-i"
  timing: "Səhər erkən"
  warnings:
    - "HƏDDƏN ARTIQ SUVARMAYIN - çiçək tökülməsinə səbəb ola bilər"
    - "Sel suvarmasından qaçının"
    - "Torpaq nəmliyini 50-60% arasında saxlayın"
message_az: "Çiçəkləmə dövrüdür. Suvarma ehtiyatla - həddən artıq su çiçək tökülməsinə səbəb olur."
```

### Qayda ORCH_IRR_002: Meyvə Böyümə Dövrü Suvarma

```yaml
rule_id: ORCH_IRR_002
name_az: "Meyvə böyümə dövrü suvarma"
name_en: "Fruit development irrigation"
priority: HIGH
applicable_to: [ORCH_APL, ORCH_GRP, ORCH_NAR, ORCH_FIG]
conditions:
  - stage == "fruit_development"
stage_specific_rules:
  apple:
    - "Həftədə 1-2 dəfə dərin suvarma"
    - "Torpaq nəmliyi 60-70%"
    - "Yığımdan 2-3 həftə əvvəl suvarmanı azaldın"
  grape:
    - "Gilə böyüməsi: müntəzəm suvarma"
    - "Veraison (rəng dəyişməsi): suvarmanı 50% azaldın"
    - "Yığımdan əvvəl: minimal suvarma (şəkər konsentrasiyası üçün)"
  pomegranate:
    - "Müntəzəm suvarma - qəfil dəyişikliklərdən qaçının"
    - "Qeyri-müntəzəm suvarma meyvə çatlamasına səbəb olur"
action:
  type: IRRIGATE
  calculation: |
    base_amount = crop_coefficient × evapotranspiration
    adjustment = temperature_factor × humidity_factor
  message_az: "{crop} üçün meyvə inkişaf dövrü. Müntəzəm suvarma vacibdir."
```

### Qayda ORCH_IRR_003: Üzüm Veraison Dövrü

```yaml
rule_id: ORCH_IRR_003
name_az: "Üzüm veraison dövrü suvarma məhdudiyyəti"
name_en: "Grape veraison irrigation restriction"
priority: HIGH
applicable_to: [ORCH_GRP]
conditions:
  - stage == "veraison" (gilələr rəng dəyişir)
action:
  type: REDUCE_IRRIGATION
  reduction: "50-70%"
  reason: "Şəkər konsentrasiyasını artırmaq və keyfiyyəti yaxşılaşdırmaq üçün"
  exceptions:
    - IF temperature > 38°C: "Minimal stres suvarması icazəli"
    - IF leaves_wilting: "Yüngül suvarma"
message_az: "Veraison dövrü. Suvarmanı azaldın - şəkər konsentrasiyası artacaq."
```

## 4.3 Gübrələmə Qaydaları

### Qayda ORCH_FERT_001: Yazda Əsas Gübrələmə

```yaml
rule_id: ORCH_FERT_001
name_az: "Yaz əsas gübrələmə"
name_en: "Spring base fertilization"
priority: HIGH
applicable_to: [ORCH_APL, ORCH_GRP, ORCH_NAR, ORCH_FIG, ORCH_PST]
conditions:
  - season == "spring"
  - stage == "bud_break" OR just_before
  - soil_temperature > 10°C
fertilizer_by_crop:
  apple:
    - NPK 12-12-17: 300-400 kg/ha
    - timing: "Tumurcuqlanmadan 2-3 həftə əvvəl"
    - method: "Tac proyeksiyası altına səpmə"
  grape:
    - NPK 10-10-10: 200-300 kg/ha
    - Ammonium sulfate: 150 kg/ha (azot mənbəyi)
    - timing: "Tumurcuqlanma əvvəli"
  pomegranate:
    - NPK 15-15-15: 200-250 kg/ha
    - timing: "Mart-Aprel"
  fig:
    - Kompost: 20-30 kg/ağac
    - NPK 10-10-10: 100-150 kg/ha
action:
  type: FERTILIZE
  message_az: "Yaz gübrələmə vaxtı. {crop} üçün {fertilizer} tövsiyə olunur."
```

### Qayda ORCH_FERT_002: Meyvə Əmələ Gəlməsindən Sonra Gübrələmə

```yaml
rule_id: ORCH_FERT_002
name_az: "Meyvə əmələ gəlməsindən sonra gübrələmə"
name_en: "Post fruit-set fertilization"
priority: MEDIUM
applicable_to: [ORCH_APL, ORCH_GRP, ORCH_NAR]
conditions:
  - stage == "fruit_set" (meyvə bağlanıb)
  - days_after_fruit_set BETWEEN 14 AND 30
fertilizer_by_crop:
  apple:
    - Calcium nitrate: 150-200 kg/ha (meyvə keyfiyyəti üçün)
    - Potassium sulfate: 100 kg/ha
    - Foliar: Bor + Kalsium spreyi
  grape:
    - Potassium sulfate: 150 kg/ha
    - Magnesium sulfate: 50 kg/ha
    - Foliar: Mikroelementlər
  pomegranate:
    - Potassium: 100-150 kg/ha (meyvə rəngi və keyfiyyəti)
    - Foliar: Kalsium (çatlamanın qarşısını almaq üçün)
action:
  type: FERTILIZE
  message_az: "Meyvə bağlanıb. Kalium və kalsium gübrələri meyvə keyfiyyətini artıracaq."
```

### Qayda ORCH_FERT_003: Yığımdan Sonra Gübrələmə

```yaml
rule_id: ORCH_FERT_003
name_az: "Yığımdan sonra bərpa gübrələməsi"
name_en: "Post-harvest recovery fertilization"
priority: MEDIUM
applicable_to: [ORCH_APL, ORCH_GRP, ORCH_NAR, ORCH_FIG]
conditions:
  - stage == "post_harvest"
  - days_after_harvest BETWEEN 7 AND 30
  - before_leaf_fall
action:
  type: FERTILIZE
  fertilizers:
    - "Azot (karbamid): 100-150 kg/ha - yarpaq funksiyasını dəstəkləyir"
    - "Fosfor: 50-100 kg/ha - kök inkişafı"
  foliar:
    - "Sink sulfat: 0.5% məhlul"
    - "Bor: 0.2% məhlul"
  reason: "Növbəti il üçün ağacın qida ehtiyatını bərpa etmək"
message_az: "Yığımdan sonra gübrələmə - ağacın bərpası və növbəti il üçün hazırlıq."
```

## 4.4 Budama Qaydaları

### Qayda ORCH_PRUNE_001: Qış Budaması

```yaml
rule_id: ORCH_PRUNE_001
name_az: "Qış budaması"
name_en: "Winter pruning"
priority: HIGH
applicable_to: [ORCH_APL, ORCH_GRP, ORCH_NAR, ORCH_FIG]
conditions:
  - stage == "dormant" (qış yuxusu)
  - temperature > -5°C (şaxta olmayan gün)
  - no_rain_forecast_48h
timing_by_crop:
  apple:
    - period: "Dekabr - Fevral"
    - avoid: "Şaxtalı günlər, tumurcuqlanma başlaması"
  grape:
    - period: "Yanvar - Fevral"
    - note: "Şirə axınından əvvəl tamamlanmalı"
  pomegranate:
    - period: "Dekabr - Yanvar"
    - note: "Yüngül budama, nar həddən artıq budamaya həssasdır"
  fig:
    - period: "Yanvar - Fevral"
    - note: "Ölü və xəstə budaqları kəsin"
action:
  type: PRUNE
  general_rules:
    - "Kəskin, dezinfeksiya olunmuş alətlər istifadə edin"
    - "Xəstə budaqları ilk kəsin və məhv edin"
    - "Kəsikləri fungisidlə örtün"
    - "Tac mərkəzini açın - işıq və hava dövranı üçün"
message_az: "Qış budama mövsümü. Şaxta olmayan gündə budama aparın."
```

### Qayda ORCH_PRUNE_002: Yay Budaması (Yaşıl Budama)

```yaml
rule_id: ORCH_PRUNE_002
name_az: "Yay yaşıl budaması"
name_en: "Summer green pruning"
priority: MEDIUM
applicable_to: [ORCH_APL, ORCH_GRP]
conditions:
  - stage == "vegetative_growth" OR "fruit_development"
  - excessive_shoot_growth == True
action:
  type: PRUNE
  grape_specific:
    - "Zoğ uclarını vurun (topping)"
    - "Salxım ətrafındakı yarpaqları seyrəldin (meyvəyə işıq düşsün)"
    - "Qoltuq zoğlarını çıxarın"
  apple_specific:
    - "Su zoğlarını (suckers) kəsin"
    - "Həddən artıq sıx budaqları seyrəldin"
message_az: "Yay budaması vaxtı. Meyvəyə işıq düşməsini təmin edin."
```

## 4.5 Zərərverici və Xəstəlik Qaydaları

### Qayda ORCH_PEST_001: Alma - Alma Güvəsi

```yaml
rule_id: ORCH_PEST_001
name_az: "Alma güvəsi riski"
name_en: "Codling moth risk for apple"
priority: HIGH
applicable_to: [ORCH_APL]
conditions:
  - stage IN ["fruit_set", "fruit_development"]
  - temperature > 15°C (gecə)
  - degree_days_accumulated > 250 (biofix-dən)
monitoring:
  - "Feromon tələləri quraşdırın"
  - "Həftəlik tələ yoxlaması"
  - "Bir tələdə 5+ güvə = müdaxilə həddi"
action:
  IF moth_count >= 5:
    type: APPLY_INSECTICIDE
    urgency: HIGH
    products:
      - "Spinosad əsaslı (üzvi)"
      - "Chlorantraniliprole"
    timing: "Yumurtadan çıxış dövrü (degree-day hesablaması ilə)"
    frequency: "7-10 gün interval"
  PREVENTIVE:
    - "Feromon pozuculuları (mating disruption)"
    - "Ağac gövdəsinə tələ kəmərləri"
message_az: "Alma güvəsi aktivdir. Feromon tələlərini yoxlayın, müdaxilə həddini izləyin."
```

### Qayda ORCH_PEST_002: Üzüm - Mildiu (Yalançı Unlu Şeh)

```yaml
rule_id: ORCH_PEST_002
name_az: "Mildiu xəstəliyi riski"
name_en: "Downy mildew risk for grape"
priority: CRITICAL
applicable_to: [ORCH_GRP]
conditions:
  - temperature BETWEEN 18°C AND 25°C
  - humidity > 85%
  - rainfall_occurred == True
  - leaf_wetness_hours > 4
risk_calculation: |
  # 10-10-10 qaydası: 10°C, 10mm yağış, 10cm zoğ böyüməsi
  risk = 0
  IF temperature > 10°C: risk += 1
  IF rainfall_last_week > 10mm: risk += 2
  IF shoot_length > 10cm: risk += 1
  IF humidity > 85%: risk += 2
  IF leaf_wetness_hours > 6: risk += 2
  
  IF risk >= 6: level = "CRITICAL"
  ELIF risk >= 4: level = "HIGH"
  ELIF risk >= 2: level = "MEDIUM"
action:
  IF level IN ["CRITICAL", "HIGH"]:
    type: APPLY_FUNGICIDE
    urgency: CRITICAL if CRITICAL else HIGH
    products:
      - "Mis əsaslı fungisidlər (Bordeaux mayesi)"
      - "Metalaxyl + Mancozeb"
      - "Fosetyl-Al"
    timing: "Yağışdan əvvəl profilaktik, yağışdan sonra müalicəvi"
    frequency: "7-10 gün (yağışdan sonra təkrar)"
  PREVENTIVE:
    - "Yarpaqların altını da çiləyin"
    - "Havalanmanı yaxşılaşdırın (budama)"
message_az: "Mildiu riski {level}. Şərait: {temp}°C, {humidity}% rütubət. Profilaktik çiləmə tövsiyə olunur."
```

### Qayda ORCH_PEST_003: Nar - Meyvə Çürüməsi

```yaml
rule_id: ORCH_PEST_003
name_az: "Nar meyvə çürüməsi riski"
name_en: "Pomegranate fruit rot risk"
priority: HIGH
applicable_to: [ORCH_NAR]
conditions:
  - stage == "fruit_development"
  - humidity > 80%
  - fruit_cracking == True
  - insect_damage == True
risk_factors:
  - "Meyvə çatlaması (suvarma qeyri-müntəzəmliyi)"
  - "Həşərat zədəsi (giriş nöqtəsi)"
  - "Yüksək rütubət"
  - "Sıx tac (havalanma zəif)"
action:
  type: PREVENTIVE
  recommendations:
    - "Suvarmanı müntəzəm edin - çatlamanın qarşısını alın"
    - "Zədəli meyvələri dərhal çıxarın"
    - "Mis fungisid çiləyin (profilaktik)"
    - "Tacı seyrəldin - hava dövranı"
message_az: "Meyvə çürüməsi riski. Çatlamış/zədəli meyvələri yığın, fungisid çiləyin."
```

---

# 📖 BÖLMƏ 5: TƏRƏVƏZÇİLİK (VEGETABLE) QAYDALARI

## 5.1 Tərəvəz Kateqoriyaları

```
VEG_ID    | Tərəvəz (AZ)  | Vegetable (EN)  | Əkin tipi
----------|---------------|-----------------|------------------
VEG_TOM   | Pomidor       | Tomato          | Açıq/Sera
VEG_CUC   | Xiyar         | Cucumber        | Açıq/Sera
VEG_PEP   | Bibər         | Pepper          | Açıq/Sera
VEG_EGG   | Badımcan      | Eggplant        | Açıq
VEG_ONI   | Soğan         | Onion           | Açıq
VEG_POT   | Kartof        | Potato          | Açıq
VEG_CAB   | Kələm         | Cabbage         | Açıq
```

## 5.2 Sera İdarəetmə Qaydaları

### Qayda VEG_GH_001: Sera Temperatur İdarəetməsi

```yaml
rule_id: VEG_GH_001
name_az: "Sera temperatur nəzarəti"
name_en: "Greenhouse temperature control"
priority: HIGH
applicable_to: [VEG_TOM, VEG_CUC, VEG_PEP] (sera şəraitində)
optimal_ranges:
  tomato:
    day: 22-28°C
    night: 15-18°C
    critical_high: 35°C
    critical_low: 10°C
  cucumber:
    day: 25-30°C
    night: 18-20°C
    critical_high: 35°C
    critical_low: 12°C
  pepper:
    day: 22-28°C
    night: 16-18°C
    critical_high: 32°C
    critical_low: 12°C
action:
  IF temperature > critical_high:
    urgency: CRITICAL
    actions:
      - "Ventilyasiyanı tam açın"
      - "Kölgələndirmə örtüyünü çəkin"
      - "Suvarma/dumanlama (cooling)"
      - "Yan pəncərələri açın"
    message_az: "KRİTİK: Sera temperaturu {temp}°C. Dərhal sovutma tədbirləri!"
  IF temperature < critical_low:
    urgency: CRITICAL
    actions:
      - "İstilik sistemini yandırın"
      - "Ventilyasiyanı bağlayın"
      - "Gecə örtüyü istifadə edin"
    message_az: "KRİTİK: Sera temperaturu {temp}°C. İstilik lazımdır!"
  IF temperature BETWEEN optimal_range:
    type: INFO
    message_az: "Temperatur optimal aralıqdadır."
```

### Qayda VEG_GH_002: Sera Rütubət İdarəetməsi

```yaml
rule_id: VEG_GH_002
name_az: "Sera rütubət nəzarəti"
name_en: "Greenhouse humidity control"
priority: HIGH
optimal_humidity:
  tomato: 60-70%
  cucumber: 70-85%
  pepper: 60-70%
action:
  IF humidity > 85%:
    urgency: HIGH
    risk: "Göbələk xəstəlikləri riski yüksək"
    actions:
      - "Ventilyasiyanı artırın"
      - "Suvarma vaxtını səhərə keçirin"
      - "Yarpaq arasını seyrəldin"
      - "Havalandırma fanları istifadə edin"
    message_az: "Rütubət çox yüksək ({humidity}%). Ventilyasiya lazımdır - xəstəlik riski!"
  IF humidity < 50%:
    urgency: MEDIUM
    actions:
      - "Damcı suvarmanı artırın"
      - "Dumanlama sistemi işladin"
      - "Döşəməni isladın"
    message_az: "Rütubət aşağıdır ({humidity}%). Çiçək tökülməsi riski."
```

## 5.3 Açıq Sahə Suvarma Qaydaları

### Qayda VEG_IRR_001: Pomidor Suvarma

```yaml
rule_id: VEG_IRR_001
name_az: "Pomidor suvarma qaydaları"
name_en: "Tomato irrigation rules"
priority: HIGH
applicable_to: [VEG_TOM]
stage_based_rules:
  transplanting_establishment:
    - frequency: "Gündəlik yüngül suvarma"
    - duration: "7-10 gün"
    - amount: "2-3 litr/bitki"
    - note: "Kök tutana qədər"
  vegetative_growth:
    - frequency: "Hər 2-3 gündən bir"
    - amount: "5-7 litr/bitki"
    - soil_moisture_target: 70%
  flowering:
    - frequency: "Hər 2 gündən bir"
    - amount: "6-8 litr/bitki"
    - warning: "Qeyri-müntəzəm suvarma çiçək tökülməsinə səbəb olur"
  fruiting:
    - frequency: "Gündəlik və ya günaşırı"
    - amount: "8-10 litr/bitki"
    - warning: "Qeyri-müntəzəm suvarma meyvə çatlamasına səbəb olur"
  ripening:
    - frequency: "Azaldın - hər 3 gündən bir"
    - reason: "Dadın yaxşılaşması üçün"
action:
  type: IRRIGATE
  method: "Damcı suvarma tövsiyə olunur"
  timing: "Səhər erkən (06:00-09:00)"
  avoid: "Yarpaq islanmasından qaçının - xəstəlik riski"
message_az: "{stage} mərhələsi. Tövsiyə: {frequency}, {amount}."
```

### Qayda VEG_IRR_002: Kartof Suvarma

```yaml
rule_id: VEG_IRR_002
name_az: "Kartof suvarma qaydaları"
name_en: "Potato irrigation rules"
priority: HIGH
applicable_to: [VEG_POT]
stage_based_rules:
  emergence:
    - frequency: "Hər 5-7 gündən bir"
    - note: "Torpağı nəm saxlayın amma su basmayın"
  vegetative:
    - frequency: "Hər 4-5 gündən bir"
    - soil_moisture: 60-70%
  tuber_initiation:
    - frequency: "Hər 3-4 gündən bir"
    - critical: "Bu dövrdə su stressi yumru sayını azaldır"
    - soil_moisture: 70-80%
  tuber_bulking:
    - frequency: "Hər 3 gündən bir"
    - critical: "Ən çox su tələb edən dövr"
    - soil_moisture: 70-80%
  maturation:
    - frequency: "Azaldın, yığımdan 2 həftə əvvəl dayandırın"
    - reason: "Qabıq bərkiməsi və saxlama keyfiyyəti üçün"
action:
  method: "Damcı və ya şırım suvarma"
  avoid: "Yarpaqların islanması - fitoftora riski"
  depth: "Dərin suvarma - kök zonası 30-40 cm"
```

## 5.4 Gübrələmə Qaydaları

### Qayda VEG_FERT_001: Pomidor Gübrələmə Proqramı

```yaml
rule_id: VEG_FERT_001
name_az: "Pomidor gübrələmə proqramı"
name_en: "Tomato fertilization program"
priority: HIGH
applicable_to: [VEG_TOM]
fertilization_schedule:
  pre_planting:
    - type: "Əsas gübrə"
    - product: "NPK 15-15-15"
    - amount: "50-60 kg/dekar"
    - timing: "Əkindən 7-10 gün əvvəl"
  
  after_transplanting:
    - type: "Starter gübrə"
    - timing: "Şitil əkimindən 10-14 gün sonra"
    - product: "Yüksək fosforlu (10-52-10)"
    - amount: "Suda həll edilmiş, hər bitkiyə 200ml"
    - purpose: "Kök inkişafı"
  
  vegetative_growth:
    - type: "Azot gübrəsi"
    - timing: "3-4 həftəlik bitkiyə"
    - product: "Kalsium ammonium nitrat"
    - amount: "25-30 kg/dekar"
    - frequency: "2 həftədən bir"
  
  flowering:
    - type: "Balanslaşdırılmış"
    - timing: "Çiçəkləmə başlayanda"
    - product: "NPK 20-20-20 + Bor"
    - method: "Yarpaq gübrəsi + torpağa"
    - note: "Bor çatışmazlığı çiçək tökülməsinə səbəb olur"
  
  fruiting:
    - type: "Kalium vurğulu"
    - timing: "Meyvələr görünəndə"
    - product: "NPK 15-10-30 və ya Kalium sulfat"
    - amount: "30-40 kg/dekar"
    - frequency: "2 həftədən bir"
    - note: "Kalium meyvə keyfiyyətini artırır"
  
  ripening:
    - type: "Kalium + Kalsium"
    - timing: "Meyvə böyüməsi zamanı"
    - product: "Kalsium nitrat + Kalium sulfat"
    - purpose: "Meyvə bərkliyi, saxlama keyfiyyəti"
  
action:
  type: FERTILIZE
  method: "Damcı suvarma ilə (fertiqasiya) və ya yarpaq gübrəsi"
```

## 5.5 Xəstəlik Qaydaları

### Qayda VEG_DIS_001: Fitoftora Riski (Kartof/Pomidor)

```yaml
rule_id: VEG_DIS_001
name_az: "Fitoftora xəstəliyi riski"
name_en: "Late blight (Phytophthora) risk"
priority: CRITICAL
applicable_to: [VEG_TOM, VEG_POT]
conditions:
  - temperature BETWEEN 10°C AND 25°C
  - humidity > 80%
  - leaf_wetness_hours > 6
  - rainfall OR heavy_dew
risk_calculation: |
  # Hutton kriteriyası
  risk = 0
  IF temperature BETWEEN 10 AND 25: risk += 2
  IF humidity > 90%: risk += 3
  ELIF humidity > 80%: risk += 2
  IF leaf_wetness_hours > 10: risk += 2
  ELIF leaf_wetness_hours > 6: risk += 1
  IF consecutive_risk_days >= 2: risk += 2
  
  IF risk >= 7: level = "CRITICAL"
  ELIF risk >= 5: level = "HIGH"
  ELIF risk >= 3: level = "MEDIUM"
symptoms:
  - "Yarpaq kənarlarından başlayan sulu ləkələr"
  - "Yarpaqlarda qəhvəyi-boz ləkələr"
  - "Ağ kif (yarpaq altında, nəm havada)"
  - "Sürətlə yayılır - günlər ərzində bütün sahə"
action:
  IF level == "CRITICAL":
    type: APPLY_FUNGICIDE
    urgency: CRITICAL
    products:
      - "Metalaxyl + Mancozeb (sistemik)"
      - "Mis hidroksid (kontakt)"
      - "Chlorothalonil"
    timing: "DƏRHAL, 7 gün interval ilə təkrar"
    message_az: "TƏCILI: Fitoftora riski kritik. Fungisid çiləyin, xəstə bitkiləri çıxarın."
  IF level == "HIGH":
    type: APPLY_FUNGICIDE
    urgency: HIGH
    products:
      - "Profilaktik mis preparatları"
      - "Mancozeb"
    timing: "Bu gün, 7-10 gün interval"
  PREVENTIVE:
    - "Yarpaqların islanmasından qaçının"
    - "Səhər tezdən suvarin - gün ərzində qurusun"
    - "Bitki arasını geniş saxlayın"
    - "Alt yarpaqları kəsin - havalanma"
```

---

# 📖 BÖLMƏ 6: QARIŞIQ TƏSƏRRÜFAT (MIXED) QAYDALARI

## 6.1 Qarışıq Təsərrüfat Konsepti

Qarışıq təsərrüfat (mixed farming) eyni sahədə həm bitkiçilik, həm heyvandarlıq aparan fermerlər üçündür. Bu, Azərbaycanda ən geniş yayılmış təsərrüfat modelidir.

## 6.2 İnteqrasiya Qaydaları

### Qayda MIX_INT_001: Peyin İdarəetməsi və Gübrələmə

```yaml
rule_id: MIX_INT_001
name_az: "Peyin idarəetməsi"
name_en: "Manure management integration"
priority: MEDIUM
conditions:
  - has_livestock == True
  - has_crops == True
  - manure_available > 0
integration_rules:
  composting:
    - "Təzə peyini birbaşa istifadə etməyin"
    - "Minimum 3-6 ay kompostlayın"
    - "Qarışdırın: peyin + saman/ot qalıqları"
    - "Temperatur 55-65°C-ə çatmalı (patogenlərin məhvi)"
  application_rates:
    - vegetables: "20-30 ton/ha (kompostlanmış)"
    - cereals: "15-20 ton/ha"
    - orchards: "10-15 kg/ağac"
  timing:
    - "Payızda torpağa qarışdırın (əkin öncəsi)"
    - "Vegetasiya dövründə istifadə etməyin"
  restrictions:
    - "Yarpaq tərəvəzlərdən 60 gün əvvəl dayandırın"
    - "Meyvə yığımından 90 gün əvvəl dayandırın"
action:
  type: MANURE_MANAGEMENT
  message_az: "Peyin ehtiyatınız var. Kompostlama və sahəyə tətbiq cədvəli yaradıldı."
```

### Qayda MIX_INT_002: Otlaq Rotasiyası

```yaml
rule_id: MIX_INT_002
name_az: "Otlaq və əkin sahəsi rotasiyası"
name_en: "Pasture and crop rotation"
priority: MEDIUM
conditions:
  - livestock_type IN [LVS_CTL, LVS_SHP, LVS_GOT]
  - has_pasture == True
  - has_crop_fields == True
rotation_rules:
  - "Yığımdan sonra sahəni heyvan otarın - anız istifadəsi"
  - "Paxlalı bitki sahəsindən sonra taxıl əkin - azot fiksasiyası"
  - "Hər 3-4 ildən bir sahə dəyişin"
  - "Kartof/pomidor sahəsini minimum 3 il heyvan otlatmayın"
benefits:
  - "Torpaq strukturunun yaxşılaşması"
  - "Gübrə xərcinin azalması"
  - "Alaq otu nəzarəti"
  - "Xəstəlik dövrünün qırılması"
message_az: "Yığım tamamlandı. Sahəni heyvanlara açmaq olar."
```

### Qayda MIX_INT_003: Gündəlik Əməliyyat Koordinasiyası

```yaml
rule_id: MIX_INT_003
name_az: "Gündəlik iş koordinasiyası"
name_en: "Daily operation coordination"
priority: HIGH
daily_schedule_logic:
  morning_priorities:
    livestock_first:
      - "05:00-06:00: Sağım (süd heyvanları)"
      - "06:00-07:00: Yemləmə"
      - "07:00-08:00: Tövlə təmizliyi"
    then_crops:
      - "08:00-10:00: Suvarma (sərin saatlarda)"
      - "08:00-10:00: Pestisid çiləmə (şeh quruduqdan sonra)"
  
  midday:
    - "10:00-16:00: İsti saatlarda ağır sahə işi yox"
    - "Heyvanlara kölgəlik/su"
    - "Ofis işləri, planlama"
  
  evening:
    - "16:00-18:00: Sahə işləri (çapa, yığım)"
    - "17:00-18:00: İkinci sağım"
    - "18:00-19:00: Axşam yemləmə"
    - "19:00-20:00: Suvarma (əgər lazımsa)"

conflict_resolution:
  - IF irrigation_critical AND milking_time:
      priority: "Sağım birinci (süd keyfiyyəti)"
      then: "Suvarmanı sağımdan sonra"
  - IF pest_urgent AND livestock_feeding:
      priority: "Yemləmə birinci"
      then: "Çiləmə səhər erkən (sabah)"
  - IF harvest_urgent AND veterinary_scheduled:
      priority: "Baytar viziti saxlayın"
      then: "Yığımı ailəyə/işçiyə həvalə edin"

message_az: "Gündəlik iş cədvəli yaradıldı. Prioritetlər: {priorities}"
```

## 6.3 Resurs Bölgüsü Qaydaları

### Qayda MIX_RES_001: Su Resurslarının Bölgüsü

```yaml
rule_id: MIX_RES_001
name_az: "Su resurslarının idarəsi"
name_en: "Water resource allocation"
priority: HIGH
conditions:
  - water_source_limited == True
  - multiple_water_needs == True
allocation_priority:
  1: 
    use: "İçməli su (heyvanlar)"
    reason: "Həyati vacib"
    cannot_skip: True
  2:
    use: "Kritik bitki suvarması (soldma əlamətləri)"
    reason: "Məhsul itkisinin qarşısı"
  3:
    use: "Planlı bitki suvarması"
    reason: "Normal inkişaf"
  4:
    use: "Tövlə yuyulması"
    reason: "Gigiyena (müntəzəm)"

drought_protocol:
  IF water_availability < 50%:
    actions:
      - "Yalnız prioritet 1-2 üçün su"
      - "Damcı suvarmaya keçin"
      - "Mulçalama tətbiq edin"
      - "Bəzi sahələri qurban verin (ən az dəyərli)"
message_az: "Su məhdudiyyəti. Prioritet sırası: İçmə suyu → Kritik suvarma → Planlı suvarma"
```

---

# 📖 BÖLMƏ 7: API SPESİFİKASİYASI

## 7.1 Endpoint-lər

```yaml
openapi: 3.0.0
info:
  title: Yonca Rule-Based Advisory API
  version: 1.0.0
  description: |
    Real data olmadan, yalnız qaydalar əsasında işləyən 
    kənd təsərrüfatı tövsiyə sistemi.
  
    Challenge Brief tələblərinə uyğun:
    - 5 farm profili dəstəyi
    - Azərbaycan dilində cavablar
    - 100% data-safety (synthetic data only)

servers:
  - url: http://localhost:8000/api/v1
    description: Development server

paths:
  /farms:
    get:
      summary: Mövcud farm profillərinin siyahısı
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FarmProfileList'
  
  /farms/{farm_type}/scenarios:
    get:
      summary: Farm tipi üçün mövcud ssenarilərin siyahısı
      parameters:
        - name: farm_type
          in: path
          required: true
          schema:
            type: string
            enum: [wheat, livestock, orchard, vegetable, mixed]
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ScenarioList'

  /recommendations:
    post:
      summary: Tövsiyə almaq
      description: |
        Farm və şərait məlumatlarına əsasən tövsiyələr qaytarır.
        Bu, əsas API endpoint-dir.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RecommendationRequest'
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RecommendationResponse'

  /schedule/daily:
    post:
      summary: Gündəlik iş cədvəli
      description: |
        Fermer üçün gündəlik iş cədvəli yaradır.
        Challenge Brief: "Fermer rutininin avtomatik schedule-ının generasiyası"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ScheduleRequest'
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DailySchedule'

  /schedule/weekly:
    post:
      summary: Həftəlik iş cədvəli
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ScheduleRequest'
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WeeklySchedule'

  /alerts:
    post:
      summary: Kritik xəbərdarlıqlar
      description: Yalnız kritik/təcili xəbərdarlıqları qaytarır
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AlertRequest'
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AlertResponse'

  /rules/{rule_id}:
    get:
      summary: Xüsusi qaydanın detalları
      parameters:
        - name: rule_id
          in: path
          required: true
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RuleDetail'

components:
  schemas:
    FarmProfile:
      type: object
      required:
        - farm_type
      properties:
        farm_type:
          type: string
          enum: [wheat, livestock, orchard, vegetable, mixed]
          description: Təsərrüfat tipi
        farm_type_az:
          type: string
          description: Azərbaycan dilində təsərrüfat tipi
        sub_type:
          type: string
          description: |
            Alt tip (məs: wheat -> winter_wheat, spring_wheat)
            livestock -> cattle, sheep, poultry
            orchard -> apple, grape, pomegranate
        area_hectares:
          type: number
          description: Sahə (hektar)
        region:
          type: string
          enum: [aran, lankaran, sheki_zagatala, ganja_gazakh, mountainous]
        irrigation_type:
          type: string
          enum: [drip, sprinkler, furrow, flood, rainfed]
  
    CropContext:
      type: object
      properties:
        crop_type:
          type: string
        stage:
          type: string
          description: Bitki mərhələsi
        days_in_stage:
          type: integer
        planting_date:
          type: string
          format: date
        days_since_irrigation:
          type: integer
        days_since_fertilization:
          type: integer
        last_pesticide_application:
          type: string
          format: date
  
    LivestockContext:
      type: object
      properties:
        animal_type:
          type: string
          enum: [cattle, sheep, goat, poultry]
        count:
          type: integer
        barn_hygiene_score:
          type: integer
          minimum: 1
          maximum: 10
        days_since_vet_check:
          type: integer
        vaccination_status:
          type: string
          enum: [current, due, overdue]
        days_since_deworming:
          type: integer
  
    WeatherContext:
      type: object
      required:
        - temperature
        - humidity
      properties:
        temperature:
          type: number
          description: Temperatur (°C)
        humidity:
          type: number
          description: Rütubət (%)
        rainfall_last_24h:
          type: number
          description: Son 24 saatda yağış (mm)
        rainfall_last_7days:
          type: number
          description: Son 7 gündə yağış (mm)
        wind_speed:
          type: number
          description: Külək sürəti (km/h)
        forecast_rain_48h:
          type: boolean
          description: Növbəti 48 saatda yağış gözlənilir
  
    SoilContext:
      type: object
      properties:
        soil_type:
          type: string
          enum: [clay, sandy, loam, clay_loam, sandy_loam]
        soil_moisture:
          type: number
          description: Torpaq nəmliyi (%)
          minimum: 0
          maximum: 100
        ph:
          type: number
          minimum: 4
          maximum: 9
  
    RecommendationRequest:
      type: object
      required:
        - farm_profile
        - weather
      properties:
        farm_profile:
          $ref: '#/components/schemas/FarmProfile'
        crop_context:
          $ref: '#/components/schemas/CropContext'
        livestock_context:
          $ref: '#/components/schemas/LivestockContext'
        weather:
          $ref: '#/components/schemas/WeatherContext'
        soil:
          $ref: '#/components/schemas/SoilContext'
        language:
          type: string
          enum: [az, en]
          default: az
  
    Recommendation:
      type: object
      properties:
        id:
          type: string
          description: Unikal tövsiyə ID
        rule_id:
          type: string
          description: Tətbiq olunan qaydanın ID-si
        action:
          type: string
          enum: [irrigate, fertilize, apply_pesticide, apply_fungicide, 
                 harvest, prune, monitor, vet_check, vaccinate, deworm,
                 adjust_feeding, improve_ventilation, no_action]
        action_az:
          type: string
          description: Azərbaycan dilində əməliyyat
        urgency:
          type: string
          enum: [critical, high, medium, low, info]
        urgency_score:
          type: integer
          minimum: 0
          maximum: 100
        message_az:
          type: string
          description: Azərbaycan dilində izahat
        message_en:
          type: string
          description: İngiliscə izahat
        timing:
          type: string
          description: Nə vaxt icra edilməli
        details:
          type: object
          description: Əlavə detallar (məs: miqdar, məhsul adı)
        reasoning:
          type: string
          description: Niyə bu tövsiyə verildi
  
    RecommendationResponse:
      type: object
      properties:
        status:
          type: string
          enum: [success, error]
        farm_type:
          type: string
        timestamp:
          type: string
          format: date-time
        critical_alerts:
          type: array
          items:
            $ref: '#/components/schemas/Recommendation'
        recommendations:
          type: array
          items:
            $ref: '#/components/schemas/Recommendation'
        metadata:
          type: object
          properties:
            rules_evaluated:
              type: integer
            rules_triggered:
              type: integer
            model_version:
              type: string
            data_source:
              type: string
              enum: [synthetic]
              description: Həmişə 'synthetic' - real data yoxdur
  
    ScheduleTask:
      type: object
      properties:
        time:
          type: string
          description: "Vaxt aralığı (məs: 06:00-08:00)"
        task:
          type: string
          description: Tapşırıq adı
        task_az:
          type: string
        priority:
          type: string
          enum: [must_do, should_do, optional]
        related_recommendation_id:
          type: string
        notes:
          type: string
  
    DailySchedule:
      type: object
      properties:
        date:
          type: string
          format: date
        farm_type:
          type: string
        morning:
          type: array
          items:
            $ref: '#/components/schemas/ScheduleTask'
        midday:
          type: array
          items:
            $ref: '#/components/schemas/ScheduleTask'
        evening:
          type: array
          items:
            $ref: '#/components/schemas/ScheduleTask'
        summary_az:
          type: string
          description: Günün xülasəsi
```

## 7.2 Request/Response Nümunələri

### Nümunə 1: Buğda Suvarma Tövsiyəsi

**Request:**

```json
{
  "farm_profile": {
    "farm_type": "wheat",
    "sub_type": "winter_wheat",
    "area_hectares": 50,
    "region": "aran",
    "irrigation_type": "drip"
  },
  "crop_context": {
    "crop_type": "wheat",
    "stage": "heading",
    "days_in_stage": 5,
    "days_since_irrigation": 4,
    "days_since_fertilization": 25
  },
  "weather": {
    "temperature": 34,
    "humidity": 40,
    "rainfall_last_24h": 0,
    "rainfall_last_7days": 0,
    "wind_speed": 10
  },
  "soil": {
    "soil_type": "clay_loam",
    "soil_moisture": 38
  },
  "language": "az"
}
```

**Response:**

```json
{
  "status": "success",
  "farm_type": "wheat",
  "timestamp": "2025-12-26T10:30:00Z",
  "critical_alerts": [
    {
      "id": "rec_001",
      "rule_id": "WHT_IRR_001",
      "action": "irrigate",
      "action_az": "Suvarma",
      "urgency": "critical",
      "urgency_score": 100,
      "message_az": "TƏCILI: Temperatur 34°C - buğda üçün kritik həddədir. Dərhal suvarma tələb olunur.",
      "message_en": "URGENT: Temperature 34°C is critical for wheat. Immediate irrigation required.",
      "timing": "Səhər 05:00-07:00 və ya axşam 19:00-21:00",
      "details": {
        "amount_mm_per_ha": 35,
        "method": "Damcı suvarma"
      },
      "reasoning": "32°C-dən yuxarı temperaturda buğda bitkisi istilik stressinə məruz qalır, bu da məhsuldarlığı 20-40% azalda bilər. Sünbülləmə mərhələsi xüsusilə həssasdır."
    }
  ],
  "recommendations": [
    {
      "id": "rec_002",
      "rule_id": "WHT_IRR_002",
      "action": "irrigate",
      "action_az": "Suvarma",
      "urgency": "high",
      "urgency_score": 80,
      "message_az": "Torpaq nəmliyi 38% - sünbülləmə mərhələsi üçün minimum 55% olmalıdır. Suvarma tövsiyə olunur.",
      "timing": "Bu gün",
      "details": {
        "target_moisture": 55,
        "current_moisture": 38
      }
    },
    {
      "id": "rec_003",
      "rule_id": "WHT_FERT_003",
      "action": "fertilize",
      "action_az": "Gübrələmə",
      "urgency": "medium",
      "urgency_score": 50,
      "message_az": "Son gübrələmədən 25 gün keçib. Sünbülləmə dövrü - yarpaq gübrəsi tövsiyə olunur.",
      "timing": "Növbəti 3-5 gün ərzində",
      "details": {
        "fertilizer": "Karbamid + Mikroelementlər",
        "method": "Yarpaq gübrələməsi",
        "amount_kg_per_ha": 50
      }
    }
  ],
  "metadata": {
    "rules_evaluated": 15,
    "rules_triggered": 3,
    "model_version": "rule_based_v1.0",
    "data_source": "synthetic"
  }
}
```

### Nümunə 2: Heyvandarlıq Xəstəlik Riski

**Request:**

```json
{
  "farm_profile": {
    "farm_type": "livestock",
    "sub_type": "dairy_cattle"
  },
  "livestock_context": {
    "animal_type": "cattle",
    "count": 50,
    "barn_hygiene_score": 5,
    "days_since_vet_check": 45,
    "vaccination_status": "due",
    "days_since_deworming": 70
  },
  "weather": {
    "temperature": 30,
    "humidity": 82
  },
  "language": "az"
}
```

**Response:**

```json
{
  "status": "success",
  "farm_type": "livestock",
  "timestamp": "2025-12-26T10:35:00Z",
  "critical_alerts": [
    {
      "id": "rec_101",
      "rule_id": "LVS_DIS_001",
      "action": "vet_check",
      "action_az": "Baytar yoxlaması",
      "urgency": "high",
      "urgency_score": 85,
      "message_az": "Mastit riski YÜKSƏK. Rütubət 82%, temperatur 30°C, gigiyena skoru 5/10. Baytar yoxlaması və gigiyena tədbirləri tövsiyə olunur.",
      "timing": "Bu gün",
      "details": {
        "risk_level": "high",
        "risk_factors": ["high_humidity", "moderate_hygiene", "heat_stress"]
      }
    }
  ],
  "recommendations": [
    {
      "id": "rec_102",
      "rule_id": "LVS_VET_001",
      "action": "vaccinate",
      "action_az": "Peyvənd",
      "urgency": "high",
      "urgency_score": 80,
      "message_az": "Peyvənd vaxtı yetişib. Baytar ilə əlaqə saxlayın.",
      "timing": "Növbəti 7 gün ərzində"
    },
    {
      "id": "rec_103",
      "rule_id": "LVS_FEED_001",
      "action": "adjust_feeding",
      "action_az": "Yemləmə tənzimləməsi",
      "urgency": "medium",
      "urgency_score": 60,
      "message_az": "İstilik stressi şəraiti (THI yüksək). Yemləməni səhər və axşam saatlarına keçirin, su girişini artırın.",
      "timing": "Bu gündən etibarən",
      "details": {
        "feed_reduction": "20%",
        "water_increase": "50%",
        "feeding_times": ["06:00", "20:00"]
      }
    },
    {
      "id": "rec_104",
      "rule_id": "LVS_VET_002",
      "action": "vet_check",
      "action_az": "Müntəzəm baytar yoxlaması",
      "urgency": "medium",
      "urgency_score": 55,
      "message_az": "Son baytar yoxlamasından 45 gün keçib. Müntəzəm yoxlama tövsiyə olunur."
    }
  ],
  "metadata": {
    "rules_evaluated": 12,
    "rules_triggered": 4,
    "model_version": "rule_based_v1.0",
    "data_source": "synthetic"
  }
}
```

### Nümunə 3: Gündəlik Cədvəl

**Request:**

```json
{
  "farm_profile": {
    "farm_type": "mixed",
    "sub_types": ["wheat", "dairy_cattle"]
  },
  "crop_context": {
    "crop_type": "wheat",
    "stage": "heading",
    "days_since_irrigation": 3
  },
  "livestock_context": {
    "animal_type": "cattle",
    "count": 30
  },
  "weather": {
    "temperature": 28,
    "humidity": 55
  },
  "date": "2025-12-27",
  "language": "az"
}
```

**Response:**

```json
{
  "date": "2025-12-27",
  "farm_type": "mixed",
  "morning": [
    {
      "time": "05:30-06:30",
      "task": "Səhər sağımı",
      "task_az": "Səhər sağımı",
      "priority": "must_do",
      "notes": "Sağımdan əvvəl yelinləri dezinfeksiya edin"
    },
    {
      "time": "06:30-07:30",
      "task": "Səhər yemləmə",
      "task_az": "Səhər yemləmə",
      "priority": "must_do"
    },
    {
      "time": "07:30-08:00",
      "task": "Tövlə təmizliyi",
      "task_az": "Tövlə təmizliyi",
      "priority": "must_do"
    },
    {
      "time": "08:00-09:30",
      "task": "Buğda sahəsini suvarma",
      "task_az": "Buğda sahəsini suvarma",
      "priority": "should_do",
      "related_recommendation_id": "rec_001",
      "notes": "Sünbülləmə dövrü - suvarma vacibdir"
    }
  ],
  "midday": [
    {
      "time": "10:00-16:00",
      "task": "İsti saatlarda ağır iş yox",
      "task_az": "İsti saatlarda ağır iş yox",
      "priority": "optional",
      "notes": "Heyvanlara kölgəlik və təzə su təmin edin"
    }
  ],
  "evening": [
    {
      "time": "17:00-18:00",
      "task": "Axşam sağımı",
      "task_az": "Axşam sağımı",
      "priority": "must_do"
    },
    {
      "time": "18:00-19:00",
      "task": "Axşam yemləmə",
      "task_az": "Axşam yemləmə",
      "priority": "must_do"
    },
    {
      "time": "19:00-20:00",
      "task": "Sahə yoxlaması",
      "task_az": "Sahə yoxlaması",
      "priority": "should_do",
      "notes": "Buğda sahəsində zərərverici əlamətlərini yoxlayın"
    }
  ],
  "summary_az": "Bu gün 3 təcili tapşırıq (sağım, yemləmə) və 2 vacib tapşırıq (suvarma, sahə yoxlaması) var. İsti hava gözlənilir - heyvanları soyuq saxlayın."
}
```

---

# 📖 BÖLMƏ 8: NEXT.JS FRONTEND STRUKTURу

İndi yuxarıdakı qaydaları və API-ni istifadə edən Next.js frontend-in tam strukturunu yaradaq.

```

```
