from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from schemas import SimulationStats, CustomScenarioRequest, WhatIfRequest
from database import get_db
from models import Sale, Inventory, Store
from sqlalchemy import func

# Simulation Engines
from simulation_engine import (
    simulate_sales_boom, 
    simulate_recession, 
    simulate_supply_shock, 
    reset_database,
    simulate_custom_scenario
)
from analysis_engine import simulate_what_if

router = APIRouter(
    prefix="/api/simulate",
    tags=["simulation"]
)

@router.post("/sales-boom")
def trigger_sales_boom(request: Request, db: Session = Depends(get_db)):
    """🚨 SİMÜLASYON: SATIŞ PATLAMASI (BOOM)"""
    msg = simulate_sales_boom(db)
    return {"message": msg, "status": "BOOM"}

@router.post("/recession")
def trigger_recession(request: Request, db: Session = Depends(get_db)):
    """📉 SİMÜLASYON: EKONOMİK DURGUNLUK (RECESSION)"""
    msg = simulate_recession(db)
    return {"message": msg, "status": "RECESSION"}

@router.post("/supply-shock")
def trigger_supply_shock(request: Request, db: Session = Depends(get_db)):
    """⚠️ SİMÜLASYON: TEDARİK ZİNCİRİ KRİZİ (SUPPLY SHOCK)"""
    msg = simulate_supply_shock(db)
    return {"message": msg, "status": "SHOCK"}

@router.post("/reset")
def trigger_reset(request: Request, db: Session = Depends(get_db)):
    """🔄 FABRİKA AYARLARINA DÖN (RESET)"""
    msg = reset_database(db)
    return {"message": msg, "status": "RESET"}

@router.get("/stats", response_model=SimulationStats)
def get_simulation_stats(db: Session = Depends(get_db)):
    # 1. Toplam Ciro
    total_revenue = db.query(func.sum(Sale.total_price)).scalar() or 0.0
    
    # 2. Toplam Stok
    total_stock = db.query(func.sum(Inventory.quantity)).scalar() or 0
    
    # 3. Kritik Mağaza Sayısı
    critical_stores = db.query(Store.id).join(Inventory).group_by(Store.id).having(func.sum(Inventory.quantity) < 100).count()
    
    return {
        "total_revenue": total_revenue,
        "total_stock": total_stock,
        "critical_stores": critical_stores
    }

@router.post("/custom")
def run_custom_simulation(scenario_req: CustomScenarioRequest, request: Request, db: Session = Depends(get_db)):
    """
    🧪 ÖZEL SENARYO SİMÜLASYONU (What-If)
    """
    result = simulate_custom_scenario(db, scenario_req.price_change, scenario_req.delay_days)
    return result

@router.post("/what-if")
def trigger_what_if(request: WhatIfRequest, db: Session = Depends(get_db)):
    return simulate_what_if(db, request.source_store_id, request.target_store_id, request.product_id, request.amount)
