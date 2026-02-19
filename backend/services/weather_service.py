import requests
import time as time_module
import logging
from core.config import settings

logger = logging.getLogger(__name__)

# Cache structure
_weather_cache = {}
WEATHER_CACHE_TTL = 3600

def get_current_weather(query: str):
    """
    Fetches weather from WeatherAPI.com with caching.
    Query can be 'Istanbul' or 'lat,lon'.
    """
    cache_key = query.lower().strip()
    now = time_module.time()
    
    # Check Cache
    if cache_key in _weather_cache:
        cached = _weather_cache[cache_key]
        if now - cached["timestamp"] < WEATHER_CACHE_TTL:
            return cached["data"]

    api_key = settings.WEATHER_API_KEY
    if not api_key:
        logger.error("WEATHER_API_KEY is missing in settings.")
        return None

    try:
        # q parameter accepts 'lat,lon'
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={query}&aqi=no&lang=tr"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current", {})
        location = data.get("location", {})
        
        result = {
            "location": location.get("name"),
            "region": location.get("region"),
            "temp_c": current.get("temp_c"),
            "condition": current.get("condition", {}).get("text"),
            "is_day": current.get("is_day") == 1,
            "code": current.get("condition", {}).get("code")
        }
        
        # Update Cache
        _weather_cache[cache_key] = {"data": result, "timestamp": now}
        return result

    except Exception as e:
        logger.error(f"Weather API Error: {e}")
        # Return stale cache if available
        if cache_key in _weather_cache:
            return _weather_cache[cache_key]["data"]
        return None
