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

    # CORS - reads from CORS_ORIGINS env variable
    # For production, set CORS_ORIGINS="https://your-frontend.onrender.com"
    # For local dev, defaults to localhost
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    # Data paths
    DATA_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    CONSTANTS_PATH: str = os.path.join(DATA_PATH, "constants")
    PROFILES_PATH: str = os.path.join(DATA_PATH, "profiles")
    RULES_PATH: str = os.path.join(DATA_PATH, "rules")

    # Debug
    DEBUG: bool = True

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS_ORIGINS string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
