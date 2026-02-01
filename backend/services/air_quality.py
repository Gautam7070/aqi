import os
import requests
from dotenv import load_dotenv

# -------------------------------------------------
# ENV SETUP
# -------------------------------------------------
load_dotenv(override=True)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "OPENWEATHER_API_KEY not found. "
        "Please set it in the .env file and restart the server."
    )

GEO_URL = "https://api.openweathermap.org/geo/1.0/direct"
AQI_URL = "https://api.openweathermap.org/data/2.5/air_pollution"


# -------------------------------------------------
# OPENWEATHER AQI INTERPRETATION (1–5)
# -------------------------------------------------
def interpret_aqi(aqi: int):
    mapping = {
        1: {"category": "Good", "meaning": "Clean air"},
        2: {"category": "Fair", "meaning": "Acceptable"},
        3: {"category": "Moderate", "meaning": "Sensitive groups affected"},
        4: {"category": "Poor", "meaning": "Health risk"},
        5: {"category": "Very Poor", "meaning": "Emergency"},
    }

    return mapping.get(
        aqi,
        {"category": "Unknown", "meaning": "Data not available"}
    )


# -------------------------------------------------
# US AQI CALCULATION (PM2.5 → 0–500)
# -------------------------------------------------
def calculate_us_aqi_pm25(pm25: float):
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 500.4, 301, 500),
    ]

    for c_lo, c_hi, i_lo, i_hi in breakpoints:
        if c_lo <= pm25 <= c_hi:
            return round(
                (i_hi - i_lo) / (c_hi - c_lo) * (pm25 - c_lo) + i_lo
            )

    return None


# -------------------------------------------------
# HEALTH RECOMMENDATIONS (US AQI BASED)
# -------------------------------------------------
def health_recommendations(aqi: int):
    if aqi <= 50:
        return {
            "risk_level": "Good",
            "recommendations": [
                "Enjoy outdoor activities",
                "No health precautions needed"
            ]
        }
    elif aqi <= 100:
        return {
            "risk_level": "Moderate",
            "recommendations": [
                "Sensitive individuals should be cautious",
                "Reduce prolonged outdoor exertion"
            ]
        }
    elif aqi <= 150:
        return {
            "risk_level": "Unhealthy for Sensitive Groups",
            "recommendations": [
                "Wear a mask if outdoors",
                "Avoid outdoor exercise",
                "Children and elderly should stay indoors"
            ]
        }
    elif aqi <= 200:
        return {
            "risk_level": "Unhealthy",
            "recommendations": [
                "Wear N95 mask",
                "Avoid morning walks",
                "Keep windows closed",
                "Use air purifiers if available"
            ]
        }
    elif aqi <= 300:
        return {
            "risk_level": "Very Unhealthy",
            "recommendations": [
                "Stay indoors",
                "Avoid all outdoor activities",
                "Use air purifiers",
                "High risk for everyone"
            ]
        }
    else:
        return {
            "risk_level": "Hazardous",
            "recommendations": [
                "Health emergency conditions",
                "Stay indoors at all times",
                "Seek medical advice if symptoms occur",
                "Avoid any physical exertion"
            ]
        }


# -------------------------------------------------
# GEO LOCATION
# -------------------------------------------------
def get_lat_lon(city: str):
    response = requests.get(
        GEO_URL,
        params={"q": city, "limit": 1, "appid": API_KEY},
        timeout=10
    )
    response.raise_for_status()

    data = response.json()
    if not data:
        return None

    return data[0]["lat"], data[0]["lon"]


# -------------------------------------------------
# AIR QUALITY DATA
# -------------------------------------------------
def get_air_quality(lat: float, lon: float):
    response = requests.get(
        AQI_URL,
        params={"lat": lat, "lon": lon, "appid": API_KEY},
        timeout=10
    )
    response.raise_for_status()

    return response.json()


# -------------------------------------------------
# MAIN SERVICE FUNCTION
# -------------------------------------------------
def get_city_air_quality(city: str):
    """
    Returns:
    - OpenWeather AQI index (1–5)
    - Real US AQI (0–500)
    - Health recommendations
    """

    location = get_lat_lon(city)
    if not location:
        return {"error": "City not found"}

    lat, lon = location
    data = get_air_quality(lat, lon)

    aqi_data = data["list"][0]
    components = aqi_data["components"]

    pm25 = components["pm2_5"]
    us_aqi = calculate_us_aqi_pm25(pm25)

    aqi_index = aqi_data["main"]["aqi"]
    index_info = interpret_aqi(aqi_index)

    health_info = health_recommendations(us_aqi)

    return {
        "city": city.capitalize(),
        "coordinates": {"lat": lat, "lon": lon},

        "aqi_index": aqi_index,        # OpenWeather (1–5)
        "us_aqi": us_aqi,              # Real AQI (0–500)

        "category": health_info["risk_level"],
        "meaning": index_info["meaning"],

        "pollutants": {
            "pm2_5": pm25,
            "pm10": components["pm10"],
            "co": round(components["co"] / 1000, 2)
        },

        "health_recommendations": health_info["recommendations"]
    }
