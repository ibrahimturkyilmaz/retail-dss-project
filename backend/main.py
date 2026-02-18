from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, get_db
from models import User
from core.logger import logger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Import Routers
from routers import (
    users, 
    sales, 
    stores, 
    products, 
    analytics, 
    simulation, 
    integrations,
    transfers
)

from core.config import settings as app_settings
import os
from dotenv import load_dotenv

load_dotenv()

# --- Limiter Setup ---
limiter = Limiter(key_func=get_remote_address, default_limits=["120/minute"])

# --- Database Setup ---
Base.metadata.create_all(bind=engine)

# --- Seeding (Simplified) ---
def seed_default_user():
    # Only runs if no admin exists
    try:
        db = next(get_db())
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            logger.info("Creating default admin user...")
            admin = User(
                username="admin",
                password="123",
                email="admin@retaildss.com",
                first_name="İbrahim",
                last_name="Türkyılmaz",
                department="Yönetim",
                role="admin"
            )
            db.add(admin)
            db.commit()
    except Exception as e:
        logger.error(f"Seeding check failed: {e}")

seed_default_user()

# --- App Init ---
app = FastAPI(title="Retail DSS API", version="2.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS ---
default_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://retail-dss-project.vercel.app"
]
env_origins = app_settings.ALLOWED_ORIGINS.split(",") if app_settings.ALLOWED_ORIGINS else []
origins = list(set(default_origins + [o.strip() for o in env_origins if o.strip()]))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routers ---
app.include_router(users.router)
app.include_router(sales.router)
app.include_router(stores.router)
app.include_router(products.router)
app.include_router(analytics.router)
app.include_router(simulation.router)
app.include_router(integrations.router)
app.include_router(transfers.router)

@app.get("/")
def read_root():
    return {"message": "Perakende Karar Destek Sistemi API Çalışıyor (Modüler Yapı v2)"}
