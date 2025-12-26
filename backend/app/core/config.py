"""
Configuration settings for Yonca API
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Yonca Rule-Based Advisory API"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000", "*"]
    
    # Data paths
    DATA_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    CONSTANTS_PATH: str = os.path.join(DATA_PATH, "constants")
    PROFILES_PATH: str = os.path.join(DATA_PATH, "profiles")
    RULES_PATH: str = os.path.join(DATA_PATH, "rules")
    
    # Debug
    DEBUG: bool = True
    
    class Config:
        case_sensitive = True


settings = Settings()
