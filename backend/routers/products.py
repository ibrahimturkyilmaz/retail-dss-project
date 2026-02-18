from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import datetime

from database import get_db
from models import Product, Forecast, Inventory, Store
from schemas import ProductSchema, NewProductSchema

router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

@router.get("", response_model=List[ProductSchema])
def read_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.post("/launch")
def launch_new_product(product: NewProductSchema, db: Session = Depends(get_db)):
    # 1. Yeni Ürünü Oluştur
    new_product = Product(
        name=product.name,
        category=product.category,
        price=product.price,
        cost=product.cost,
        abc_category="C" # Yeni ürün başlangıçta C olur
    )
    db.add(new_product)
    db.commit() # ID almak için commit
    
    # 2. Referans Ürün Verilerini Kullan (Cold Start)
    if product.reference_product_id:
        ref_product = db.query(Product).filter(Product.id == product.reference_product_id).first()
        if ref_product:
            # ABC Kategorisini kopyala (Beklenti bu yönde ise)
            new_product.abc_category = ref_product.abc_category
            
            # Referans ürünün tahminlerini %80 oranıyla kopyala (Training Data)
            # Not: Gerçek hayatta bu daha karmaşık bir ML modelidir.
            today = datetime.date.today()
            ref_forecasts = db.query(Forecast).filter(
                Forecast.product_id == ref_product.id,
                Forecast.date >= today
            ).all()
            
            for rf in ref_forecasts:
                new_forecast = Forecast(
                    store_id=rf.store_id,
                    product_id=new_product.id,
                    date=rf.date,
                    predicted_quantity=rf.predicted_quantity * 0.8 # %80 varsayımı
                )
                db.add(new_forecast)
                
    # 3. Envanter Kayıtlarını Aç (Stok 0)
    stores = db.query(Store).all()
    for store in stores:
        inv = Inventory(store_id=store.id, product_id=new_product.id, quantity=0, safety_stock=10)
        db.add(inv)
        
    db.commit()
    return {"message": "Yeni ürün lansmanı başarıyla yapıldı", "product_id": new_product.id}
