from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from core.config import settings

# --- 1. ASYNC ENGINE (FastAPI Endpointleri İçin) ---
# URL Dönüşümü: sqlite -> sqlite+aiosqlite, postgresql -> postgresql+asyncpg
ASYNC_DB_URL = settings.DATABASE_URL
if "sqlite" in ASYNC_DB_URL and "+aiosqlite" not in ASYNC_DB_URL:
    ASYNC_DB_URL = ASYNC_DB_URL.replace("sqlite://", "sqlite+aiosqlite://")
elif "postgresql" in ASYNC_DB_URL and "+asyncpg" not in ASYNC_DB_URL:
    ASYNC_DB_URL = ASYNC_DB_URL.replace("postgresql://", "postgresql+asyncpg://")

# Connect args for SQLite
# Connect args
connect_args = {}
if "sqlite" in ASYNC_DB_URL:
    connect_args = {"check_same_thread": False}
else:
    # PostgreSQL (PgBouncer) uyumluluğu
    connect_args = {"statement_cache_size": 0}

async_engine = create_async_engine(
    ASYNC_DB_URL,
    echo=settings.TESTING,
    future=True,
    connect_args=connect_args
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# --- 2. SYNC ENGINE (Pandas & Legacy Analiz İçin) ---
# Pandas read_sql henüz async desteklemiyor, bu yüzden sync engine'i tutuyoruz.
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

Base = declarative_base()

# --- BACKWARD COMPATIBILITY ---
engine = sync_engine

# --- DEPENDENCIES ---

async def get_db():
    """
    Asenkron veritabanı oturumu sağlar.
    FastAPI 'async def' endpointlerinde bunu kullanın.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_sync_db():
    """
    Senkron veritabanı oturumu sağlar.
    Pandas işlemleri veya 'def' endpointlerinde bunu kullanın.
    """
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
