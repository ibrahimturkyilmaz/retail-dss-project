from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_engine, Base, get_db, get_sync_db
from models import User
from core.logger import logger
from core.config import settings
from core.exceptions import RetailException, ResourceNotFoundException
from core.handlers import global_exception_handler, retail_exception_handler, not_found_handler
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import contextlib

# Import Routers
from routers import (
    users,
    sales,
    stores,
    products,
    analytics,
    simulation,
    integrations,
    transfers,
    pos,
    customers, # Phase 8
    marketing # Phase 2 (New)
)





# --- Lifespan Events (Startup/Shutdown) ---
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Tabloları oluştur (Async)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed Data (Sync olarak çalıştırılabilir veya Async'e çevrilebilir)
    # Basitlik için Sync Session kullanıyoruz
    seed_default_user()
    
    yield
    # Shutdown

# --- Seeding ---
def seed_default_user():
    try:
        # Sync DB kullanıyoruz çünkü startup scripti
        db = next(get_sync_db())
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

# --- App Init ---
app = FastAPI(
    title=settings.PROJECT_NAME, 
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# --- Exception Handlers ---
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RetailException, retail_exception_handler)
app.add_exception_handler(ResourceNotFoundException, not_found_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- Limiter ---
limiter = Limiter(key_func=get_remote_address, default_limits=["120/minute"])
app.state.limiter = limiter

# --- CORS ---
origins = settings.ALLOWED_ORIGINS.split(",")

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
# app.include_router(simulation.router)
app.include_router(integrations.router)
app.include_router(transfers.router)
app.include_router(pos.router)
app.include_router(customers.router) # Phase 8
app.include_router(marketing.router) # Phase 2 (New)

@app.get("/")
async def read_root(): 
    return {"message": f"{settings.PROJECT_NAME} API Çalışıyor (Async Mode)"}
