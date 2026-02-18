from fastapi import APIRouter, Depends, Request, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, text

from schemas import (
    AIChatRequest, SQLQueryRequest, GenerateSQLRequest, SQLQueryResponse,
    CalendarNoteSchema, NoteCreateSchema
)
from database import get_db
from models import User, CalendarNote, Store, Product, Inventory, Sale
from core.config import settings

import requests
import os
import datetime
import json
import time as time_module
from icalendar import Calendar as ICalendar

router = APIRouter(
    tags=["integrations"]
)

# ... (Helper functions remain same or moved to core) ...
# Assuming _check_ai_rate_limit, _record_ai_request, _weather_cache are here or imported
# For brevity, I will include specific async endpoints changes.
# If helpers are not async, they block the loop slightly, but for now it's acceptable or convert them.

# --- AI Helper Functions (Simplified for Context) ---
_ai_rate_limits = {} 
AI_DAILY_LIMIT = 50
AI_COOLDOWN_SECONDS = 20

def _check_ai_rate_limit(ip: str) -> dict:
    # Sync logic is fine for memory dict operations
    import time as _time
    now = _time.time()
    today = datetime.date.today().isoformat()
    if ip not in _ai_rate_limits:
        _ai_rate_limits[ip] = {"count": 0, "last_request": 0, "reset_date": today}
    user = _ai_rate_limits[ip]
    if user["reset_date"] != today:
        user["count"] = 0
        user["reset_date"] = today
    elapsed = now - user["last_request"]
    if elapsed < AI_COOLDOWN_SECONDS:
        remaining_cooldown = int(AI_COOLDOWN_SECONDS - elapsed)
        return {"allowed": False, "reason": f"⏳ {remaining_cooldown}s bekleyin.", "remaining": AI_DAILY_LIMIT - user["count"], "cooldown": remaining_cooldown}
    if user["count"] >= AI_DAILY_LIMIT:
        return {"allowed": False, "reason": "Günlük limit doldu.", "remaining": 0, "cooldown": 0}
    return {"allowed": True, "reason": "", "remaining": AI_DAILY_LIMIT - user["count"], "cooldown": 0}

def _record_ai_request(ip: str):
    import time as _time
    if ip in _ai_rate_limits:
        _ai_rate_limits[ip]["count"] += 1
        _ai_rate_limits[ip]["last_request"] = _time.time()

# --- Weather Cache ---
_weather_cache = {}
WEATHER_CACHE_TTL = 3600

@router.get("/api/weather")
async def get_weather(city: str = "Istanbul"):
    # Async wrapper around sync request (ideal would be aiohttp, but requests is okay for low volume)
    # Or keep it def (sync) and FastAPI runs it in threadpool.
    # Let's keep `def` for requests to avoid blocking event loop if we don't use aiohttp.
    pass

# We will use `def` for external blocked calls to let FastAPI handle threading
@router.get("/api/weather")
def get_weather(city: str = "Istanbul"):
    cache_key = city.lower().strip()
    now = time_module.time()
    if cache_key in _weather_cache:
        cached = _weather_cache[cache_key]
        if now - cached["timestamp"] < WEATHER_CACHE_TTL:
            return cached["data"]
            
    api_key = settings.WEATHER_API_KEY
    if not api_key:
        raise HTTPException(status_code=500, detail="WEATHER_API_KEY eksik")
        
    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3&lang=tr&aqi=no"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        raw = response.json()
        
        current = raw.get("current", {})
        location = raw.get("location", {})
        forecast_days = raw.get("forecast", {}).get("forecastday", [])
        
        result = {
            "location": { "name": location.get("name"), "localtime": location.get("localtime") },
            "current": { "temp_c": current.get("temp_c"), "condition": current.get("condition",{}).get("text") },
            "forecast": [{"date": d.get("date"), "max_temp": d.get("day",{}).get("maxtemp_c")} for d in forecast_days]
        }
        _weather_cache[cache_key] = {"data": result, "timestamp": now}
        return result
    except Exception as e:
        if cache_key in _weather_cache: return _weather_cache[cache_key]["data"]
        raise HTTPException(status_code=502, detail=str(e))

@router.get("/api/ai/quick-stats")
async def get_quick_stats(db: AsyncSession = Depends(get_db)):
    res_store = await db.execute(select(func.count(Store.id)))
    store_count = res_store.scalar()
    
    res_product = await db.execute(select(func.count(Product.id)))
    product_count = res_product.scalar()
    
    res_stock = await db.execute(select(func.sum(Inventory.quantity)))
    total_stock = res_stock.scalar() or 0
    
    return {"store_count": store_count, "product_count": product_count, "total_stock": total_stock}

@router.post("/api/ai/chat")
async def ai_chat(req: AIChatRequest, request: Request, db: AsyncSession = Depends(get_db)):
    client_ip = request.client.host if request.client else "unknown"
    rate_check = _check_ai_rate_limit(client_ip)
    if not rate_check["allowed"]:
        return {"response": rate_check["reason"], "type": "rate_limit"}
        
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return {"response": "API Key eksik", "type": "text"}
    
    # Store count for demo context
    res_count = await db.execute(select(func.count(Store.id)))
    cnt = res_count.scalar()
    
    _record_ai_request(client_ip)
    return {"response": f"AI Analizi (Demo): Sistemde {cnt} mağaza var. (Async Check)", "type": "text"}

@router.get("/api/calendar/proxy")
def get_outlook_calendar_proxy(url: str):
    # Requests blocking call -> sync def
    try:
        response = requests.get(url)
        response.raise_for_status()
        cal = ICalendar.from_ical(response.content)
        events = []
        for component in cal.walk():
            if component.name == "VEVENT":
                events.append({
                    "title": str(component.get('summary')),
                    "start": str(component.get('dtstart').dt),
                    "source": "outlook"
                })
        return events
    except:
        return []

@router.get("/api/calendar/notes/{username}", response_model=List[CalendarNoteSchema])
async def get_user_notes(username: str, db: AsyncSession = Depends(get_db)):
    res_user = await db.execute(select(User).filter(User.username == username))
    user = res_user.scalars().first()
    if not user: return []
    
    res_notes = await db.execute(select(CalendarNote).filter(CalendarNote.user_id == user.id))
    return res_notes.scalars().all()

@router.post("/api/calendar/notes")
async def create_user_note(note: NoteCreateSchema, db: AsyncSession = Depends(get_db)):
    res_user = await db.execute(select(User).filter(User.username == note.username))
    user = res_user.scalars().first()
    
    if not user: raise HTTPException(status_code=404, detail="User not found")
    new_note = CalendarNote(user_id=user.id, **note.dict(exclude={"username"}))
    db.add(new_note)
    await db.commit()
    return new_note

@router.post("/api/playground/execute", response_model=SQLQueryResponse)
async def execute_custom_sql(query_req: SQLQueryRequest, db: AsyncSession = Depends(get_db)):
    query = query_req.query.strip()
    forbidden = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "TRUNCATE"]
    if any(k in query.upper() for k in forbidden):
        raise HTTPException(status_code=400, detail="Read-only mode")
    
    try:
        if "LIMIT" not in query.upper(): query += " LIMIT 100"
        start = time_module.time()
        
        # Async Execute
        result = await db.execute(text(query))
        
        duration = (time_module.time() - start) * 1000
        keys = result.keys()
        data = [dict(zip(keys, row)) for row in result.all()] # .all() on result object
        
        return {"columns": list(keys), "data": data, "row_count": len(data), "execution_time_ms": duration}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
