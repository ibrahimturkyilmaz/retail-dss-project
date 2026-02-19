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

@router.get("/api/weather")
def get_weather_endpoint(city: str = "Istanbul"):
    # Use centralized service
    from services.weather_service import get_current_weather
    
    # city can be city name or lat,lon
    weather = get_current_weather(city)
    
    if not weather:
        raise HTTPException(status_code=502, detail="Hava durumu servisi hatası")
        
    return {
        "location": {"name": weather["location"]},
        "current": {"temp_c": weather["temp_c"], "condition": weather["condition"]}
    }
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
