"""
Pydantic models for Yonca API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from datetime import datetime
from datetime import date as date_type


# ============== ENUMS ==============

class FarmType(str, Enum):
    WHEAT = "wheat"
    LIVESTOCK = "livestock"
    ORCHARD = "orchard"
    VEGETABLE = "vegetable"
    MIXED = "mixed"


class UrgencyLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AnimalType(str, Enum):
    CATTLE = "cattle"
    SHEEP = "sheep"
    GOAT = "goat"
    POULTRY = "poultry"


class Region(str, Enum):
    ARAN = "aran"
    LANKARAN = "lankaran"
    SHEKI_ZAGATALA = "sheki_zagatala"
    GANJA_GAZAKH = "ganja_gazakh"
    MOUNTAINOUS = "mountainous"


# ============== WEATHER ==============

class WeatherData(BaseModel):
    """Weather information"""
    temperature: float = Field(..., description="Temperatur (°C)")
    humidity: float = Field(..., ge=0, le=100, description="Rütubət (%)")
    rainfall_last_24h: float = Field(default=0, ge=0, description="Son 24 saat yağış (mm)")
    rainfall_last_7days: float = Field(default=0, ge=0, description="Son 7 gün yağış (mm)")
    rainfall_forecast_48h: bool = Field(default=False, description="48 saatda yağış gözlənilir")
    rainfall_forecast_amount_mm: float = Field(default=0, description="Gözlənilən yağış miqdarı (mm)")
    wind_speed: float = Field(default=0, ge=0, description="Külək sürəti (km/saat)")
    frost_warning: bool = Field(default=False, description="Şaxta xəbərdarlığı")
    time_of_day: Optional[str] = Field(default=None, description="Günün vaxtı (morning/midday/evening/night)")


# ============== SOIL ==============

class SoilData(BaseModel):
    """Soil information"""
    soil_moisture: float = Field(..., ge=0, le=100, description="Torpaq nəmliyi (%)")
    soil_temperature: Optional[float] = Field(default=None, description="Torpaq temperaturu (°C)")
    soil_type: Optional[str] = Field(default=None, description="Torpaq tipi")
    ph: Optional[float] = Field(default=None, ge=0, le=14, description="Torpaq pH")


# ============== CROP CONTEXT ==============

class CropContext(BaseModel):
    """Crop/plant context information"""
    crop_type: str = Field(..., description="Bitki növü (wheat, tomato, grape, etc.)")
    stage: str = Field(..., description="İnkişaf mərhələsi")
    days_in_stage: int = Field(default=0, ge=0, description="Mərhələdə gün sayı")
    days_since_irrigation: int = Field(default=0, ge=0, description="Son suvarmadan keçən gün")
    days_since_fertilization: int = Field(default=0, ge=0, description="Son gübrələmədən keçən gün")
    days_until_harvest: Optional[int] = Field(default=None, description="Yığıma qalan gün")
    growing_type: Optional[str] = Field(default="open_field", description="open_field or greenhouse")
    
    # Optional fields for specific conditions
    grain_moisture: Optional[float] = Field(default=None, description="Dən rütubəti (%)")
    grain_shattering: Optional[bool] = Field(default=False, description="Dən tökülməsi")
    nitrogen_deficiency_signs: Optional[bool] = Field(default=False, description="Azot çatışmazlığı əlamətləri")
    calcium_deficiency_signs: Optional[bool] = Field(default=False, description="Kalsium çatışmazlığı əlamətləri")
    aphid_count_per_head: Optional[int] = Field(default=None, description="Sünbüldə mənənə sayı")
    seed_treated: Optional[bool] = Field(default=True, description="Toxum dərmanlanıb")
    diseased_branches_present: Optional[bool] = Field(default=False, description="Xəstə budaqlar var")
    previous_crop: Optional[str] = Field(default=None, description="Əvvəlki bitki")
    tree_age_years: Optional[int] = Field(default=None, description="Ağac yaşı")
    days_after_harvest: Optional[int] = Field(default=None, description="Yığımdan sonra gün")


# ============== GREENHOUSE ==============

class GreenhouseContext(BaseModel):
    """Greenhouse-specific context"""
    inside_temperature: float = Field(..., description="Daxili temperatur (°C)")
    inside_humidity: float = Field(..., ge=0, le=100, description="Daxili rütubət (%)")
    ventilation_status: str = Field(default="open", description="Ventilyasiya (open/closed/auto)")
    heating_status: Optional[str] = Field(default="off", description="İsitmə (on/off/auto)")


# ============== LIVESTOCK ==============

class LivestockContext(BaseModel):
    """Livestock context information"""
    animal_type: AnimalType = Field(..., description="Heyvan növü")
    count: int = Field(default=1, ge=1, description="Heyvan sayı")
    barn_hygiene_score: int = Field(..., ge=1, le=10, description="Tövlə gigiyena skoru (1-10)")
    days_since_vet_check: int = Field(default=0, ge=0, description="Son baytar yoxlamasından gün")
    vaccination_status: str = Field(default="current", description="Peyvənd statusu (current/due/overdue)")
    days_since_deworming: int = Field(default=0, ge=0, description="Son dərmanlama")
    ventilation_quality: str = Field(default="good", description="Ventilyasiya (good/adequate/poor)")
    water_availability: str = Field(default="adequate", description="Su mövcudluğu")
    
    # Optional fields
    lactation_stage: Optional[str] = Field(default=None, description="Laktasiya mərhələsi (early/mid/late/dry)")
    reproductive_stage: Optional[str] = Field(default=None, description="Reproduktiv mərhələ")
    days_until_expected_birth: Optional[int] = Field(default=None, description="Doğuma qalan gün")
    age_days: Optional[int] = Field(default=None, description="Yaş (gün)")


# ============== RESOURCE CONTEXT ==============

class ResourceContext(BaseModel):
    """Resource availability context for mixed farms"""
    water_availability: str = Field(default="adequate", description="Su (adequate/limited/scarce)")
    labor_availability: str = Field(default="adequate", description="Əmək (adequate/limited)")
    financial_status: str = Field(default="normal", description="Maliyyə (normal/tight)")


# ============== FARM COMPONENTS (for mixed farms) ==============

class FarmComponents(BaseModel):
    """Farm components for mixed farms"""
    crop_types: List[str] = Field(default=[], description="Bitki növləri")
    livestock_types: List[str] = Field(default=[], description="Heyvan növləri")


# ============== MAIN REQUEST ==============

class RecommendationRequest(BaseModel):
    """Main request for getting recommendations"""
    farm_type: FarmType = Field(..., description="Ferma tipi")
    region: Region = Field(..., description="Region")
    request_date: date_type = Field(default_factory=date_type.today, description="Tarix")
    
    # Weather data
    weather: WeatherData = Field(..., description="Hava məlumatları")
    
    # Soil data (optional for livestock)
    soil: Optional[SoilData] = Field(default=None, description="Torpaq məlumatları")
    
    # Context based on farm type
    crop_context: Optional[CropContext] = Field(default=None, description="Bitki konteksti")
    livestock_context: Optional[LivestockContext] = Field(default=None, description="Heyvandarlıq konteksti")
    greenhouse_context: Optional[GreenhouseContext] = Field(default=None, description="Sera konteksti")
    
    # For mixed farms
    resource_context: Optional[ResourceContext] = Field(default=None, description="Resurs konteksti")
    farm_components: Optional[FarmComponents] = Field(default=None, description="Ferma komponentləri")


# ============== RECOMMENDATIONS OUTPUT ==============

class RecommendationAction(BaseModel):
    """A single recommended action"""
    rule_id: str
    name_az: str
    name_en: str
    category: str
    urgency: UrgencyLevel
    urgency_score: int = Field(ge=0, le=100)
    message_az: str
    message_en: str
    action_type: str
    action_details: Optional[Dict[str, Any]] = None
    timing_az: Optional[str] = None


class DailyScheduleItem(BaseModel):
    """A scheduled item for the day"""
    time_slot: str
    task_az: str
    task_en: str
    priority: str
    related_rule_id: Optional[str] = None
    urgency_score: int = Field(ge=0, le=100)


class RecommendationResponse(BaseModel):
    """Response with all recommendations"""
    farm_type: FarmType
    region: Region
    response_date: date_type
    generated_at: datetime = Field(default_factory=datetime.now)
    
    # Grouped recommendations
    critical_alerts: List[RecommendationAction] = []
    high_priority: List[RecommendationAction] = []
    medium_priority: List[RecommendationAction] = []
    low_priority: List[RecommendationAction] = []
    info: List[RecommendationAction] = []
    
    # Daily schedule
    daily_schedule: List[DailyScheduleItem] = []
    
    # Summary
    total_recommendations: int = 0
    summary_az: str = ""
    summary_en: str = ""


# ============== SIMPLE ENDPOINTS ==============

class FarmProfileResponse(BaseModel):
    """Farm profile information"""
    farm_type: str
    sub_types: List[str]
    required_inputs: List[str]
    rule_categories: List[Dict[str, Any]]


class RuleInfo(BaseModel):
    """Basic rule information"""
    rule_id: str
    name_az: str
    name_en: str
    priority: str
    category: str
    farm_type: str


class RulesListResponse(BaseModel):
    """List of all rules"""
    total_rules: int
    rules_by_category: Dict[str, List[RuleInfo]]


class ConstantsResponse(BaseModel):
    """Constants information"""
    stages: Dict[str, Any]
    regions: Dict[str, Any]
    thresholds: Dict[str, Any]
