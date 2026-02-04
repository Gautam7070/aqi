import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from services.air_quality import (
    get_lat_lon,
    get_air_quality,
    calculate_us_aqi_pm25,
    health_recommendations
)

# -------------------------
# App Initialization
# -------------------------
app = FastAPI(title="Air Quality API")

# -------------------------
# Enable CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Root Health Check (IMPORTANT for Render)
# -------------------------
@app.get("/")
def root():
    return {"status": "Backend running successfully"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# -------------------------
# AQI Endpoint
# -------------------------
@app.get("/air-quality")
def air_quality(city: str):
    # 1️⃣ Get coordinates
    coords = get_lat_lon(city)
    if not coords:
        raise HTTPException(
            status_code=404,
            detail="Invalid city name or data not available"
        )

    lat, lon = coords

    # 2️⃣ Get air quality data
    data = get_air_quality(lat, lon)
    aqi_data = data["list"][0]
    components = aqi_data["components"]

    # 3️⃣ Calculate REAL AQI (US AQI 0–500)
    pm25 = components["pm2_5"]
    us_aqi = calculate_us_aqi_pm25(pm25)

    # 4️⃣ Health recommendations
    health = health_recommendations(us_aqi)

    # 5️⃣ Final response
    return {
        "city": city.capitalize(),
        "aqi": us_aqi,
        "risk_level": health["risk_level"],
        "pollutants": {
            "pm2_5": pm25,
            "pm10": components["pm10"],
            "co": round(components["co"] / 1000, 2)  # µg/m³ → mg/m³
        },
        "health_recommendations": health["recommendations"]
    }

# -------------------------
# Render-Compatible Startup
# -------------------------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
