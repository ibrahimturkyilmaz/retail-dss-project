from fastapi import APIRouter, HTTPException
import json
import urllib.request
import urllib.parse
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/utils",
    tags=["Utils"]
)

class GeocodeRequest(BaseModel):
    lat: float
    lon: float

@router.get("/proxy/reverse-geocode")
async def reverse_geocode(lat: float, lon: float):
    """
    Proxy request to Nominatim to avoid CORS issues on frontend.
    """
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
        headers = {'User-Agent': 'RetailDSSApp/1.0 (contact: admin@retaildss.com)'}
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
