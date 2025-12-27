/**
 * Weather Service - Auto-fetch weather based on IP location
 * Uses Open-Meteo (free, no API key) and ipapi.co (free IP geolocation)
 */

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
}

/**
 * Get user's location from IP address
 */
export async function getLocationFromIP(): Promise<LocationData> {
  try {
    const response = await fetch('https://ipapi.co/json/', {
      headers: {
        'Accept': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch location');
    }

    const data = await response.json();

    return {
      latitude: data.latitude,
      longitude: data.longitude,
      city: data.city,
      country: data.country_name,
      region: data.region,
    };
  } catch (error) {
    console.error('IP geolocation error:', error);
    throw new Error('Could not determine location from IP');
  }
}

/**
 * Fetch current weather data from Open-Meteo
 */
export async function fetchWeatherData(latitude: number, longitude: number): Promise<Omit<WeatherResult, 'location'>> {
  try {
    // Open-Meteo API - free, no API key required
    const url = new URL('https://api.open-meteo.com/v1/forecast');
    url.searchParams.set('latitude', latitude.toString());
    url.searchParams.set('longitude', longitude.toString());
    url.searchParams.set('current', 'temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m');
    url.searchParams.set('timezone', 'auto');
    url.searchParams.set('forecast_days', '1');

    const response = await fetch(url.toString());

    if (!response.ok) {
      throw new Error('Failed to fetch weather data');
    }

    const data = await response.json();
    const current = data.current;

    // Check for frost warning (temperature below 0°C)
    const frost_warning = current.temperature_2m < 0;

    return {
      temperature: Math.round(current.temperature_2m),
      humidity: Math.round(current.relative_humidity_2m),
      rainfall_last_24h: current.precipitation || 0,
      wind_speed: Math.round(current.wind_speed_10m),
      frost_warning,
    };
  } catch (error) {
    console.error('Weather API error:', error);
    throw new Error('Could not fetch weather data');
  }
}

/**
 * Auto-fetch weather based on user's IP location
 */
export async function autoFetchWeather(): Promise<WeatherResult> {
  try {
    // Step 1: Get location from IP
    const location = await getLocationFromIP();

    // Step 2: Fetch weather for that location
    const weather = await fetchWeatherData(location.latitude, location.longitude);

    return {
      ...weather,
      location,
    };
  } catch (error) {
    console.error('Auto-fetch weather error:', error);
    throw error;
  }
}

/**
 * Map Azerbaijan region names to region codes
 */
export function mapLocationToRegion(city: string, region: string): string {
  const cityLower = city?.toLowerCase() || '';
  const regionLower = region?.toLowerCase() || '';

  // Direct city mappings
  if (cityLower.includes('ganja') || cityLower.includes('gəncə') || cityLower.includes('gazakh')) {
    return 'ganja_gazakh';
  }
  if (cityLower.includes('lankaran') || cityLower.includes('lənkəran') || cityLower.includes('astara')) {
    return 'lankaran';
  }
  if (cityLower.includes('sheki') || cityLower.includes('şəki') || cityLower.includes('zagatala') || cityLower.includes('zaqatala') || cityLower.includes('balakan') || cityLower.includes('qax')) {
    return 'sheki_zagatala';
  }
  if (cityLower.includes('quba') || cityLower.includes('qusar') || cityLower.includes('xinaliq') || cityLower.includes('qabala')) {
    return 'mountainous';
  }

  // Region-based mappings
  if (regionLower.includes('ganja') || regionLower.includes('gəncə') || regionLower.includes('gazakh')) {
    return 'ganja_gazakh';
  }
  if (regionLower.includes('lankaran') || regionLower.includes('lənkəran')) {
    return 'lankaran';
  }
  if (regionLower.includes('sheki') || regionLower.includes('şəki') || regionLower.includes('zagatala')) {
    return 'sheki_zagatala';
  }
  if (regionLower.includes('quba') || regionLower.includes('mountain')) {
    return 'mountainous';
  }

  // Default to Aran (central region)
  return 'aran';
}
