"""
Weather Service - Auto-fetch weather based on IP location
Handles external API calls for IP geolocation and weather data
"""

import httpx
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for fetching weather data based on IP location"""

    IPAPI_URL = "https://ipapi.co/json/"
    OPENMETEO_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

    async def get_location_from_ip(self, client_ip: Optional[str] = None) -> Dict[str, Any]:
        """
        Get user's location from IP address

        Args:
            client_ip: Optional IP address (for debugging)

        Returns:
            Location data with latitude, longitude, city, country
        """
        try:
            response = await self.client.get(
                self.IPAPI_URL,
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            data = response.json()

            return {
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "city": data.get("city", "Unknown"),
                "country": data.get("country_name", "Unknown"),
                "region": data.get("region", "")
            }
        except Exception as e:
            logger.error(f"IP geolocation error: {e}")
            raise ValueError("Could not determine location from IP")

    async def fetch_weather_data(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Fetch current weather data from Open-Meteo

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            Weather data with temperature, humidity, rainfall, wind speed
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
                "timezone": "auto",
                "forecast_days": "1"
            }

            response = await self.client.get(self.OPENMETEO_URL, params=params)
            response.raise_for_status()
            data = response.json()

            current = data.get("current", {})

            # Check for frost warning (temperature below 0°C)
            temperature = current.get("temperature_2m", 0)
            frost_warning = temperature < 0

            return {
                "temperature": round(temperature),
                "humidity": round(current.get("relative_humidity_2m", 0)),
                "rainfall_last_24h": current.get("precipitation", 0),
                "wind_speed": round(current.get("wind_speed_10m", 0)),
                "frost_warning": frost_warning
            }
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            raise ValueError("Could not fetch weather data")

    async def auto_fetch_weather(self, client_ip: Optional[str] = None) -> Dict[str, Any]:
        """
        Auto-fetch weather based on user's IP location

        Args:
            client_ip: Optional IP address (for debugging)

        Returns:
            Combined location and weather data
        """
        try:
            # Step 1: Get location from IP
            location = await self.get_location_from_ip(client_ip)

            # Step 2: Fetch weather for that location
            weather = await self.fetch_weather_data(
                location["latitude"],
                location["longitude"]
            )

            return {
                **weather,
                "location": location
            }
        except Exception as e:
            logger.error(f"Auto-fetch weather error: {e}")
            raise

    def map_location_to_region(self, city: str, region: str) -> str:
        """
        Map Azerbaijan location to region codes

        Args:
            city: City name
            region: Region name

        Returns:
            Region code (aran, lankaran, sheki_zagatala, ganja_gazakh, mountainous)
        """
        city_lower = city.lower() if city else ""
        region_lower = region.lower() if region else ""

        # Direct city mappings
        if any(x in city_lower for x in ["ganja", "gəncə", "gazakh"]):
            return "ganja_gazakh"
        if any(x in city_lower for x in ["lankaran", "lənkəran", "astara"]):
            return "lankaran"
        if any(x in city_lower for x in ["sheki", "şəki", "zagatala", "zaqatala", "balakan", "qax"]):
            return "sheki_zagatala"
        if any(x in city_lower for x in ["quba", "qusar", "xinaliq", "qabala"]):
            return "mountainous"

        # Region-based mappings
        if any(x in region_lower for x in ["ganja", "gəncə", "gazakh"]):
            return "ganja_gazakh"
        if any(x in region_lower for x in ["lankaran", "lənkəran"]):
            return "lankaran"
        if any(x in region_lower for x in ["sheki", "şəki", "zagatala"]):
            return "sheki_zagatala"
        if any(x in region_lower for x in ["quba", "mountain"]):
            return "mountainous"

        # Default to Aran (central region)
        return "aran"
