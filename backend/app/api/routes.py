"""
API Routes for Yonca Rule-Based Advisory System
"""

from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any, List, Optional

from app.models.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    FarmProfileResponse,
    RulesListResponse,
    RuleInfo,
    ConstantsResponse,
    FarmType,
    Region
)
from app.services.rule_engine import RuleEngine
from app.services.weather_service import WeatherService


router = APIRouter()


# ============== RECOMMENDATIONS ==============

@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: Request, data: RecommendationRequest):
    """
    Get personalized recommendations based on farm context.
    
    Bu endpoint fermerin şərtlərinə əsaslanaraq tövsiyələr verir.
    """
    # Get loaded rules and constants from app state
    rules = request.app.state.rules
    constants = request.app.state.constants
    
    # Create rule engine and evaluate
    engine = RuleEngine(rules, constants)
    response = engine.evaluate(data)
    
    return response


@router.get("/recommendations/quick")
async def quick_recommendations(
    request: Request,
    farm_type: FarmType,
    region: Region,
    temperature: float,
    humidity: float,
    crop_type: Optional[str] = None,
    stage: Optional[str] = None,
    days_since_irrigation: int = 0,
    soil_moisture: float = 50
):
    """
    Quick recommendation endpoint with minimal parameters.
    
    Sadə sorğu üçün - yalnız əsas parametrlərlə.
    """
    from app.models.schemas import WeatherData, SoilData, CropContext
    from datetime import date
    
    # Build request object
    weather = WeatherData(temperature=temperature, humidity=humidity)
    soil = SoilData(soil_moisture=soil_moisture)
    
    crop_context = None
    if crop_type and stage:
        crop_context = CropContext(
            crop_type=crop_type,
            stage=stage,
            days_since_irrigation=days_since_irrigation
        )
    
    data = RecommendationRequest(
        farm_type=farm_type,
        region=region,
        request_date=date.today(),
        weather=weather,
        soil=soil,
        crop_context=crop_context
    )
    
    # Get loaded rules and constants from app state
    rules = request.app.state.rules
    constants = request.app.state.constants
    
    # Create rule engine and evaluate
    engine = RuleEngine(rules, constants)
    response = engine.evaluate(data)
    
    return response


# ============== WEATHER ==============

@router.get("/weather/auto")
async def auto_fetch_weather(request: Request):
    """
    Automatically fetch weather data based on client's IP location.
    Falls back to Baku, Azerbaijan if IP geolocation fails (rate limit, etc.)

    IP əsasında avtomatik hava məlumatı əldə edilməsi.
    IP geolocation uğursuz olsa Bakı məlumatları qaytarılır.

    Returns:
        - temperature: Current temperature (°C)
        - humidity: Relative humidity (%)
        - rainfall_last_24h: Rainfall in last 24h (mm)
        - wind_speed: Wind speed (km/h)
        - frost_warning: Boolean frost warning
        - location: Detected location (city, country, lat/lng)
        - region: Mapped Azerbaijan region code
        - fallback: Boolean indicating if default location was used
    """
    weather_service = WeatherService()

    try:
        # Get client IP from request (for production with proxy/load balancer)
        client_ip = request.client.host if request.client else None

        # Auto-fetch weather and location (gracefully falls back to Baku if IP geolocation fails)
        result = await weather_service.auto_fetch_weather(client_ip)

        # Map location to Azerbaijan region
        region = weather_service.map_location_to_region(
            result["location"]["city"],
            result["location"].get("region", "")
        )

        # Check if we used fallback location
        is_fallback = result["location"]["city"] == "Bakı" and result["location"]["country"] == "Azerbaijan"

        return {
            "temperature": result["temperature"],
            "humidity": result["humidity"],
            "rainfall_last_24h": result["rainfall_last_24h"],
            "wind_speed": result["wind_speed"],
            "frost_warning": result["frost_warning"],
            "location": result["location"],
            "region": region,
            "fallback": is_fallback  # Indicates if default location was used
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data: {str(e)}")
    finally:
        await weather_service.close()


# ============== FARMS & PROFILES ==============

@router.get("/farms")
async def list_farm_types():
    """
    List all available farm types.
    
    Bütün mövcud ferma tiplərinin siyahısı.
    """
    return {
        "farm_types": [
            {
                "id": "wheat",
                "name_az": "Taxıl təsərrüfatı",
                "name_en": "Wheat/Cereals Farm",
                "description_az": "Buğda, arpa və digər dənli bitkilər"
            },
            {
                "id": "livestock",
                "name_az": "Heyvandarlıq",
                "name_en": "Livestock Farm",
                "description_az": "Mal-qara, qoyun, keçi, quşçuluq"
            },
            {
                "id": "orchard",
                "name_az": "Meyvə bağı",
                "name_en": "Orchard",
                "description_az": "Alma, üzüm, nar, əncir və digər meyvələr"
            },
            {
                "id": "vegetable",
                "name_az": "Tərəvəzçilik",
                "name_en": "Vegetable Farm",
                "description_az": "Pomidor, xiyar, kartof və digər tərəvəzlər"
            },
            {
                "id": "mixed",
                "name_az": "Qarışıq təsərrüfat",
                "name_en": "Mixed Farm",
                "description_az": "Bitkiçilik və heyvandarlıq birlikdə"
            }
        ]
    }


@router.get("/farms/{farm_type}/profile", response_model=FarmProfileResponse)
async def get_farm_profile(request: Request, farm_type: FarmType):
    """
    Get detailed profile for a farm type.
    
    Ferma tipi haqqında ətraflı məlumat.
    """
    profiles = request.app.state.profiles
    profile = profiles.get(farm_type.value)
    
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile not found for {farm_type.value}")
    
    return FarmProfileResponse(
        farm_type=farm_type.value,
        sub_types=profile.get('sub_types', []),
        required_inputs=profile.get('required_inputs', []),
        rule_categories=profile.get('rule_categories', [])
    )


# ============== RULES ==============

@router.get("/rules/search")
async def search_rules(request: Request, q: str):
    """
    Search rules by keyword.
    
    Qaydaları açar söz ilə axtarın.
    """
    rule_loader = request.app.state.rule_loader
    results = rule_loader.search_rules(q)
    
    return {
        "query": q,
        "count": len(results),
        "results": results
    }


@router.get("/rules")
async def list_all_rules(request: Request):
    """
    List all available rules grouped by farm type and category.
    
    Bütün qaydaların siyahısı.
    """
    rules = request.app.state.rules
    rule_loader = request.app.state.rule_loader
    
    counts = rule_loader.count_rules()
    
    rules_by_category = {}
    
    for farm_type, categories in rules.items():
        rules_by_category[farm_type] = {}
        for category, data in categories.items():
            if data and 'rules' in data:
                rules_by_category[farm_type][category] = [
                    RuleInfo(
                        rule_id=r.get('rule_id', ''),
                        name_az=r.get('name_az', ''),
                        name_en=r.get('name_en', ''),
                        priority=r.get('priority', 'medium'),
                        category=category,
                        farm_type=farm_type
                    )
                    for r in data['rules']
                ]
    
    return {
        "total_rules": counts.get('_total', 0),
        "counts_by_farm_type": {k: v for k, v in counts.items() if k != '_total'},
        "rules_by_category": rules_by_category
    }


@router.get("/rules/{farm_type}")
async def get_rules_by_farm_type(request: Request, farm_type: FarmType):
    """
    Get all rules for a specific farm type.
    
    Xüsusi ferma tipi üçün qaydalar.
    """
    rule_loader = request.app.state.rule_loader
    farm_rules = rule_loader.get_rules_for_farm_type(farm_type.value)
    
    if not farm_rules:
        raise HTTPException(status_code=404, detail=f"No rules found for {farm_type.value}")
    
    return {
        "farm_type": farm_type.value,
        "categories": list(farm_rules.keys()),
        "rules": farm_rules
    }


@router.get("/rules/{farm_type}/{category}")
async def get_rules_by_category(request: Request, farm_type: FarmType, category: str):
    """
    Get rules for a specific farm type and category.
    
    Xüsusi kateqoriya üçün qaydalar.
    """
    rule_loader = request.app.state.rule_loader
    farm_rules = rule_loader.get_rules_for_farm_type(farm_type.value)
    
    if not farm_rules or category not in farm_rules:
        raise HTTPException(
            status_code=404, 
            detail=f"No rules found for {farm_type.value}/{category}"
        )
    
    return farm_rules[category]


# ============== CONSTANTS ==============

@router.get("/constants")
async def get_all_constants(request: Request):
    """
    Get all constant values (thresholds, regions, stages).
    
    Bütün sabit dəyərləri əldə edin.
    """
    constants = request.app.state.constants
    return constants


@router.get("/constants/thresholds")
async def get_thresholds(request: Request):
    """
    Get threshold values for various conditions.
    
    Hədd dəyərləri (temperatur, rütubət və s.).
    """
    rule_loader = request.app.state.rule_loader
    return rule_loader.get_thresholds()


@router.get("/constants/regions")
async def get_regions(request: Request):
    """
    Get information about Azerbaijan regions.
    
    Azərbaycan regionları haqqında məlumat.
    """
    rule_loader = request.app.state.rule_loader
    return rule_loader.get_regions()


@router.get("/constants/stages")
async def get_stages(request: Request):
    """
    Get crop/livestock growth stages.
    
    Bitki və heyvan inkişaf mərhələləri.
    """
    rule_loader = request.app.state.rule_loader
    return rule_loader.get_stages()


# ============== SCENARIOS ==============

@router.get("/scenarios/{farm_type}")
async def get_test_scenarios(request: Request, farm_type: FarmType):
    """
    Get predefined test scenarios for a farm type.
    
    Test üçün hazır ssenarilər.
    """
    profiles = request.app.state.profiles
    profile = profiles.get(farm_type.value)
    
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile not found for {farm_type.value}")
    
    scenarios = profile.get('synthetic_scenarios', {})
    
    return {
        "farm_type": farm_type.value,
        "scenarios": scenarios
    }


# ============== STATISTICS ==============

@router.get("/stats")
async def get_statistics(request: Request):
    """
    Get system statistics.
    
    Sistem statistikaları.
    """
    rule_loader = request.app.state.rule_loader
    counts = rule_loader.count_rules()
    
    return {
        "total_rules": counts.get('_total', 0),
        "rules_by_farm_type": {
            k: v.get('_total', 0) 
            for k, v in counts.items() 
            if k != '_total' and isinstance(v, dict)
        },
        "farm_types_count": 5,
        "regions_count": 5,
        "rule_categories": {
            "wheat": ["irrigation", "fertilization", "pest_disease", "harvest"],
            "livestock": ["disease_risk", "feeding", "veterinary"],
            "orchard": ["irrigation", "fertilization", "pruning", "pest_disease"],
            "vegetable": ["irrigation", "fertilization", "greenhouse", "pest_disease"],
            "mixed": ["integration", "resource_allocation", "daily_coordination"]
        }
    }
