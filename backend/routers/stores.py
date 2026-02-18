from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from typing import List
import datetime

from database import get_db
from models import Store, Inventory, Forecast, Product
from schemas import StoreSchema, InventorySchema

router = APIRouter(
    prefix="/api/stores",
    tags=["stores"]
)

@router.get("", response_model=List[StoreSchema])
async def read_stores(db: AsyncSession = Depends(get_db)):
    """
    🏪 MAĞAZALARI LİSTELE
    """
    # Features ve Inventory ilişkisini eager load yapıyoruz
    stmt = select(Store).options(
        selectinload(Store.features),
        selectinload(Store.inventory)
    )
    result = await db.execute(stmt)
    stores = result.scalars().all()
    
    # Risk Analizi ve Stok Hesaplama
    for store in stores:
        # Toplam Stok ve Güvenlik Stoğu
        total_stock = sum(i.quantity for i in store.inventory)
        total_safety = sum(i.safety_stock for i in store.inventory)
        
        # Pydantic model bunları bekliyor, dinamik olarak ekliyoruz
        store.stock = total_stock
        store.safety_stock = total_safety
        
        # Risk Analizi
        # Stoğu 10'un altında olan kaç çeşit ürün var?
        result_risk = await db.execute(
            select(func.count(Inventory.id)).filter(
                Inventory.store_id == store.id,
                Inventory.quantity < 10
            )
        )
        risk_count = result_risk.scalar() or 0
        
        if risk_count > 20:
            store.risk_status = "CRITICAL"
        elif risk_count > 5:
            store.risk_status = "WARNING"
        else:
            store.risk_status = "SAFE"
            
    return stores

@router.get("/{store_id}/inventory", response_model=List[InventorySchema])
async def get_store_inventory(store_id: int, db: AsyncSession = Depends(get_db)):
    """
    📦 MAĞAZA STOK DURUMU
    """
    # Ürün detaylarını ve Gelecek Tahminlerini (Forecast) dahil et
    stmt = select(Inventory).filter(Inventory.store_id == store_id).options(
        selectinload(Inventory.product)
    )
    result = await db.execute(stmt)
    inventory_items = result.scalars().all()
    
    # Tahminleri al (Sonraki ay için)
    next_month = datetime.date.today() + datetime.timedelta(days=30)
    
    for item in inventory_items:
        # Bu ürün için bu mağazadaki toplam tahmin
        result_forecast = await db.execute(
            select(func.sum(Forecast.predicted_quantity)).filter(
                Forecast.store_id == store_id,
                Forecast.product_id == item.product_id,
                Forecast.date <= next_month
            )
        )
        total_forecast = result_forecast.scalar() or 0
        
        # Dinamik özellik ekleme (Schema'da varsa)
        item.predicted_sales = total_forecast
        
        # Stok yetersiz mi?
        if item.quantity < total_forecast:
            item.status = "OUT_OF_STOCK_RISK"
        elif item.quantity > total_forecast * 2:
            item.status = "OVERSTOCK"
        else:
            item.status = "OPTIMAL"
            
    return inventory_items
