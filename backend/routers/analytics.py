from fastapi import APIRouter, Depends, Response, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
import datetime
import io
import csv

from database import get_sync_db
from models import Sale, Product, Forecast
from schemas import AnalyticsResponse, InventorySchema
# Helper functions from original main.py imports (moved or assumed accessible)
from analysis_engine import calculate_abc_analysis, simulate_what_if, calculate_forecast_accuracy
from cold_start_engine import analyze_cold_start
from export_engine import export_training_data

router = APIRouter(
    tags=["analytics"]
)

@router.get("/api/sales/analytics", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_sync_db)):
    """
    📊 GELİŞMİŞ SATIŞ ANALİTİĞİ
    """
    # Toplam Ciro
    total_revenue = db.query(func.sum(Sale.total_price)).scalar() or 0.0
    
    # Toplam İşlem Sayısı
    total_transactions = db.query(func.count(Sale.id)).scalar() or 0
    
    # En Çok Satan Ürün
    top_product_id = db.query(Sale.product_id, func.count(Sale.product_id).label('count'))\
        .group_by(Sale.product_id)\
        .order_by(func.count(Sale.product_id).desc())\
        .first()
        
    top_product_name = "Yok"
    if top_product_id:
        product = db.query(Product).filter(Product.id == top_product_id[0]).first()
        if product:
            top_product_name = product.name
            
    return {
        "total_revenue": total_revenue,
        "top_selling_product": top_product_name,
        "total_transactions": total_transactions
    }

@router.get("/api/forecast")
def get_forecasts(store_id: int = None, product_id: int = None, db: Session = Depends(get_sync_db)):
    """
    📈 TAHMİN SONUÇLARI
    """
    query = db.query(Forecast).join(Product).join(Store)
    
    if store_id:
        query = query.filter(Forecast.store_id == store_id)
    if product_id:
        query = query.filter(Forecast.product_id == product_id)
        
    forecasts = query.limit(200).all()
    
    results = []
    for f in forecasts:
        results.append({
            "store": f.store.name,
            "product": f.product.name,
            "date": f.date,
            "prediction": f.predicted_quantity,
            "is_proxy": False, 
            "confidence": "HIGH" if f.predicted_quantity > 0 else "MEDIUM"
        })
    return results

@router.get("/api/analysis/accuracy")
def get_forecast_accuracy(store_id: int, product_id: int, db: Session = Depends(get_sync_db)):
    return calculate_forecast_accuracy(db, store_id, product_id)

@router.get("/api/analysis/cold-start")
def get_cold_start_analysis(product_id: int, db: Session = Depends(get_sync_db)):
    return analyze_cold_start(db, product_id)

@router.get("/api/analysis/abc")
def get_abc_analysis(db: Session = Depends(get_sync_db)):
    return calculate_abc_analysis(db)

@router.get("/api/analysis/model-metrics")
def get_model_metrics(store_id: int = 1, product_id: int = 1, db: Session = Depends(get_sync_db)):
    today = datetime.date.today()
    forecasts = db.query(Forecast).filter(
        Forecast.store_id == store_id, 
        Forecast.product_id == product_id,
        Forecast.date >= today
    ).all()
    
    if not forecasts:
        return {
            "model_name": "Prophet (Henüz veri yok)",
            "avg_confidence": 0,
            "confidence_level": "Bilinmiyor",
            "last_training": "Yok",
            "forecast_horizon": "7 Gün"
        }
    
    avg_score = sum(f.confidence_score or 0 for f in forecasts) / len(forecasts)
    
    if avg_score > 85: level = "Yüksek (High)"
    elif avg_score > 60: level = "Orta (Medium)"
    else: level = "Düşük (Low)"
        
    return {
        "model_name": forecasts[0].model_name or "Prophet",
        "avg_confidence": round(avg_score, 1),
        "confidence_level": level,
        "last_training": datetime.date.today().strftime("%Y-%m-%d"), 
        "forecast_horizon": f"{len(forecasts)} Gün"
    }

@router.get("/api/export/training-data")
def get_training_data(store_id: int, product_id: int, db: Session = Depends(get_sync_db)):
    csv_content = export_training_data(db, store_id, product_id)
    
    if not csv_content:
        raise HTTPException(status_code=404, detail="Satış verisi bulunamadı")
        
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=sales_s{store_id}_p{product_id}.csv"}
    )
