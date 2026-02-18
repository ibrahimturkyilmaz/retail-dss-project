from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import datetime

from database import get_db
from models import Store, Inventory, Forecast
from schemas import StoreSchema, InventorySchema

router = APIRouter(
    prefix="/api/stores",
    tags=["stores"]
)

@router.get("", response_model=List[StoreSchema])
def read_stores(db: Session = Depends(get_db)):
    """
    🏪 MAĞAZA LİSTESİ VE DURUM ANALİZİ
    """
    stores = db.query(Store).all()
    
    # [OPTIMIZASYON] Risk raporunu tek seferde çek (Bulk SQL)
    from risk_engine import get_risk_report
    risk_report = get_risk_report(db, stores)
    
    # Raporu ID ile eşleştir
    risk_map = {r["store_id"]: r for r in risk_report}
    
    results = []
    for store in stores:
        # Önceden hesaplanmış rapordan veriyi al
        stats = risk_map.get(store.id, {})
        
        results.append({
            "id": store.id,
            "name": store.name,
            "store_type": store.store_type,
            "lat": store.lat,
            "lon": store.lon,
            "stock": stats.get("stock", 0),
            "safety_stock": stats.get("safety_stock", 0),
            "risk_status": stats.get("status", "UNKNOWN")
        })
    return results

@router.get("/{store_id}/inventory", response_model=List[InventorySchema])
def get_store_inventory(store_id: int, db: Session = Depends(get_db)):
    """
    📦 MAĞAZA ENVANTERİ VE TAHMİNLER
    """
    inventory = db.query(Inventory).filter(Inventory.store_id == store_id).all()
    results = []
    
    # Bugünün tarihi
    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)

    for item in inventory:
        # Sonraki 7 günün tahminini topla
        forecast_sum = db.query(func.sum(Forecast.predicted_quantity))\
            .filter(Forecast.store_id == store_id, 
                    Forecast.product_id == item.product_id,
                    Forecast.date >= today,
                    Forecast.date < next_week)\
            .scalar() or 0.0

        results.append({
            "product_id": item.product.id,
            "product_name": item.product.name,
            "category": item.product.category,
            "quantity": item.quantity,
            "safety_stock": item.safety_stock,
            "abc_category": item.product.abc_category or "C",
            "forecast_next_7_days": round(forecast_sum, 1)
        })
    return results
