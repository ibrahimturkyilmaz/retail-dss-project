from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Store, Product, Customer, Sale, Forecast, Inventory
from pydantic import BaseModel
from typing import List, Optional
import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

app = FastAPI()

# CORS Ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class StoreSchema(BaseModel):
    id: int
    name: str
    store_type: str # Enum string olarak dönecek
    lat: float
    lon: float
    stock: int
    safety_stock: int
    risk_status: str

    class Config:
        from_attributes = True

class TransferRequest(BaseModel):
    source_store_id: int
    target_store_id: int
    product_id: int # Şimdilik stok genel tutuluyor ama ürün bazlı transfer için parametre
    amount: int

class AnalyticsResponse(BaseModel):
    total_revenue: float
    top_selling_product: str
    total_transactions: int

from risk_engine import analyze_store_risk, get_risk_report
from transfer_engine import generate_transfer_recommendations
from simulation_engine import simulate_sales_boom, simulate_recession, simulate_supply_shock, reset_database

class SaleSchema(BaseModel):
    id: int
    store_name: str
    product_name: str
    customer_name: str
    date: datetime.date
    quantity: int
    total_price: float

    class Config:
        from_attributes = True

# --- API Endpoints ---

from models import Store, Product, Customer, Sale, Forecast, Inventory

@app.get("/api/sales", response_model=List[SaleSchema])
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sales = db.query(Sale).order_by(Sale.date.desc()).offset(skip).limit(limit).all()
    
    results = []
    for s in sales:
        results.append({
            "id": s.id,
            "store_name": s.store.name if s.store else "Bilinmiyor",
            "product_name": s.product.name if s.product else "Bilinmiyor",
            "customer_name": s.customer.name if s.customer else "Bilinmiyor",
            "date": s.date,
            "quantity": s.quantity,
            "total_price": s.total_price
        })
    return results

@app.get("/stores", response_model=List[StoreSchema])
def read_stores(db: Session = Depends(get_db)):
    stores = db.query(Store).all()
    results = []
    for store in stores:
        # Eski basit mantık yerine Risk Motorunu kullanıyoruz
        status = analyze_store_risk(store)
        
        # Envanterden toplam stok ve güvenlik stoğunu hesapla
        total_stock = sum(item.quantity for item in store.inventory)
        total_safety = sum(item.safety_stock for item in store.inventory)

        results.append({
            "id": store.id,
            "name": store.name,
            "store_type": store.store_type,
            "lat": store.lat,
            "lon": store.lon,
            "stock": total_stock,
            "safety_stock": total_safety,
            "risk_status": status
        })
    return results

@app.get("/api/transfers/recommendations", response_model=List[TransferRecommendationSchema])
def get_transfer_recommendations(db: Session = Depends(get_db)):
    stores = db.query(Store).all()
    # Demo için sadece ilk 50 mağazayı analiz edelim (Performans)
    recommendations = generate_transfer_recommendations(stores[:50]) 
    return recommendations

@app.post("/api/transfer")
def transfer_stock(request: TransferRequest, db: Session = Depends(get_db)):
    # 1. Kaynak ve Hedef mağazayı bul
    source = db.query(Store).filter(Store.id == request.source_store_id).first()
    target = db.query(Store).filter(Store.id == request.target_store_id).first()
    
    if not source or not target:
        raise HTTPException(status_code=404, detail="Mağaza bulunamadı")
        
    # 2. Ürün bazlı stok kontrolü (Veya genel stok - şimdilik genel demo için basitleştirilmiş)
    # Gelişmiş versiyonda request.product_id kullanılmalı
    
    # Basitlik için: Eğer product_id verilmişse o ürünü transfer et, yoksa hata ver
    if request.product_id:
        source_item = db.query(Inventory).filter(Inventory.store_id == source.id, Inventory.product_id == request.product_id).first()
        target_item = db.query(Inventory).filter(Inventory.store_id == target.id, Inventory.product_id == request.product_id).first()
        
        if not source_item:
             raise HTTPException(status_code=400, detail="Kaynak mağazada bu ürün yok")
             
        if not target_item:
            # Hedefte ürün yoksa oluştur (Sıfır stokla)
            target_item = Inventory(store_id=target.id, product_id=request.product_id, quantity=0, safety_stock=10) # safety default
            db.add(target_item)
            
        if source_item.quantity < request.amount:
            raise HTTPException(status_code=400, detail=f"Kaynak mağazada yetersiz stok (Mevcut: {source_item.quantity})")
            
        source_item.quantity -= request.amount
        target_item.quantity += request.amount
        
        product_name = source_item.product.name
        msg = f"{source.name} şubesinden {target.name} şubesine {request.amount} adet {product_name} transfer edildi."

    else:
        # Legacy/Test modu (Eski frontend isteği atarsa)
        # Sadece hata döndürelim, çünkü artık stoklar sadece inventory tablosunda
        raise HTTPException(status_code=400, detail="Transfer için product_id zorunludur.")
    
    db.commit()
    return {"message": msg}

@app.get("/api/sales/analytics", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    # Toplam Ciro
    total_revenue = db.query(func.sum(Sale.total_price)).scalar() or 0.0
    
    # Toplam İşlem Sayısı
    total_transactions = db.query(func.count(Sale.id)).scalar() or 0
    
    # En Çok Satan Ürün
    # sales tablosunda product_id'ye göre grupla, count al, en büyüğü seç
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

@app.post("/api/forecast/generate")
def generate_forecasts(db: Session = Depends(get_db)):
    """
    Basit Lineer Regresyon ile önümüzdeki 30 günün talebini tahmin eder.
    Her Mağaza ve Ürün kombinasyonu için çalışır.
    """
    # Önce eski tahminleri temizle (Basitlik için)
    db.query(Forecast).delete()
    db.commit()
    
    stores = db.query(Store).all()
    # Şimdilik çok ürün var, performans için sadece ilk 5 ürüne tahmin yapalım demo amaçlı
    products = db.query(Product).limit(5).all() 
    
    generated_count = 0
    
    for store in stores:
        for product in products:
            # Geçmiş satış verilerini çek
            sales_data = db.query(Sale.date, Sale.quantity)\
                .filter(Sale.store_id == store.id, Sale.product_id == product.id)\
                .order_by(Sale.date)\
                .all()
            
            if len(sales_data) < 10: # Yeterli veri yoksa atla
                continue
                
            # Pandas DataFrame oluştur
            df = pd.DataFrame(sales_data, columns=['date', 'quantity'])
            df['date_ordinal'] = pd.to_datetime(df['date']).map(datetime.datetime.toordinal)
            
            # Model Eğitimi
            X = df[['date_ordinal']]
            y = df['quantity']
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Gelecek 30 gün için tahmin
            last_date = pd.to_datetime(df['date'].max())
            future_dates = [last_date + timedelta(days=x) for x in range(1, 31)]
            future_ordinals = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
            
            predictions = model.predict(future_ordinals)
            
            # Veritabanına kaydet
            for i, pred in enumerate(predictions):
                # Negatif tahminleri sıfırla
                pred_qty = max(0, round(pred))
                
                forecast = Forecast(
                    store_id=store.id,
                    product_id=product.id,
                    date=future_dates[i],
                    predicted_quantity=pred_qty
                )
                db.add(forecast)
                generated_count += 1
                
    db.commit()
    return {"message": f"{generated_count} adet günlük tahmin oluşturuldu."}

@app.get("/api/forecast")
def get_forecasts(db: Session = Depends(get_db)):
    forecasts = db.query(Forecast).join(Product).join(Store).limit(100).all()
    
    results = []
    for f in forecasts:
        results.append({
            "store": f.store.name,
            "product": f.product.name,
            "date": f.date,
            "prediction": f.predicted_quantity
        })
    return results

@app.get("/")
def read_root():
    return {"message": "Perakende Karar Destek Sistemi API Çalışıyor (Faz 1)"}

# --- Simulation Endpoints ---

@app.post("/api/simulate/sales-boom")
def trigger_sales_boom(db: Session = Depends(get_db)):
    msg = simulate_sales_boom(db)
    return {"message": msg, "status": "BOOM"}

@app.post("/api/simulate/recession")
def trigger_recession(db: Session = Depends(get_db)):
    msg = simulate_recession(db)
    return {"message": msg, "status": "RECESSION"}

@app.post("/api/simulate/supply-shock")
def trigger_supply_shock(db: Session = Depends(get_db)):
    msg = simulate_supply_shock(db)
    return {"message": msg, "status": "SHOCK"}

@app.post("/api/simulate/reset")
def trigger_reset(db: Session = Depends(get_db)):
    msg = reset_database(db)
    return {"message": msg, "status": "RESET"}

class SimulationStats(BaseModel):
    total_revenue: float
    total_stock: int
    critical_stores: int

@app.get("/api/simulate/stats", response_model=SimulationStats)
def get_simulation_stats(db: Session = Depends(get_db)):
    # 1. Toplam Ciro
    total_revenue = db.query(func.sum(Sale.total_price)).scalar() or 0.0
    
    # 2. Toplam Stok
    total_stock = db.query(func.sum(Inventory.quantity)).scalar() or 0
    
    # 3. Kritik Mağaza Sayısı (Basitçe toplam stoğu 500'den az olanlar diyelim - Demo için)
    # Daha gelişmişi: risk_engine ile hepsini taramak ama o yavaş olabilir.
    # SQL ile hızlı sayım:
    critical_stores = db.query(Store.id).join(Inventory).group_by(Store.id).having(func.sum(Inventory.quantity) < 100).count()
    
    return {
        "total_revenue": total_revenue,
        "total_stock": total_stock,
        "critical_stores": critical_stores
    }

