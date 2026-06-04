import requests
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

load_dotenv()
API_KEY = os.getenv("API_KEY")
forecast_base_url = "https://api.openweathermap.org/data/2.5/forecast"
geocoding_base_url = "https://api.openweathermap.org/geo/1.0/direct"

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(os.getenv("REDIS_URL"))
    FastAPICache.init(RedisBackend(redis), prefix="weather-cache")
    yield
    await redis.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:63342"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/forecast")
@cache(expire=600)
def get_forecast(lat: float, lon: float) -> dict:
    url = f"{forecast_base_url}"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(url, params=params, timeout=(3.05, 10))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Weather API timeout. Please try again later."
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to connect to Weather API. Please try again later."
        )
    except requests.exceptions.HTTPError as e:
        if e.response is not None:
            if e.response.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid API key."
                )
            if e.response.status_code == 429:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests. Please try again later."
                )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Weather API error."
        )
    except (requests.exceptions.RequestException, ValueError):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to retrieve weather data."
        )

@app.get("/geocoords/{city_name}")
@cache(expire=86400)
def get_geocoords(city_name: str) -> dict:
    url = f"{geocoding_base_url}"
    params = {
        "q": city_name,
        "limit": 1,
        "appid": API_KEY
    }
    try:
        response = requests.get(url, params=params, timeout=(3.05, 10))
        response.raise_for_status()

        data = response.json()
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City '{city_name}' not found."
            )

        data = data[0]
        latitude = data["lat"]
        longitude = data["lon"]
        return {"lat": latitude, "lon": longitude}
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Geocoding API timeout. Please try again later."
        )
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key."
            )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Geocoding API error."
        )
    except (requests.exceptions.RequestException, ValueError):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to retrieve geocoding data."
        )