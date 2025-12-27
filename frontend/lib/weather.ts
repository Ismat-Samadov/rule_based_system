/**
 * Weather Service - Auto-fetch weather based on IP location
 * Calls backend API which handles external API requests
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface LocationData {
  latitude: number;
  longitude: number;
  city: string;
  country: string;
  region?: string;
}

export interface WeatherResult {
  temperature: number;
  humidity: number;
  rainfall_last_24h: number;
  wind_speed: number;
  frost_warning: boolean;
  location: LocationData;
  region: string;
}

/**
 * Auto-fetch weather based on user's IP location
 * This calls the backend endpoint which handles external API calls
 */
export async function autoFetchWeather(): Promise<WeatherResult> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/weather/auto`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Failed to fetch weather data');
    }

    const data = await response.json();

    return {
      temperature: data.temperature,
      humidity: data.humidity,
      rainfall_last_24h: data.rainfall_last_24h,
      wind_speed: data.wind_speed,
      frost_warning: data.frost_warning,
      location: data.location,
      region: data.region,
    };
  } catch (error) {
    console.error('Auto-fetch weather error:', error);
    throw error;
  }
}

