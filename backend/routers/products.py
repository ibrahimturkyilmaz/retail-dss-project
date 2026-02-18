from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
import datetime

from database import get_db
from models import Product, Forecast, Inventory, Store
from schemas import ProductSchema, NewProductSchema

# Simulation engine import (Assuming it has a synchronous implementation, 
# we might need to be careful if it uses DB inside)
# from simulation_engine import handle_cold_start # Bu modülün async olup olmadığını kontrol etmeliyiz.

router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

@router.get("", response_model=List[ProductSchema])
async def read_products(db: AsyncSession = Depends(get_db)):
    """
    🏷️ ÜRÜNLERİ LİSTELE
    """
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products

@router.post("/launch")
async def launch_new_product(product: NewProductSchema, db: AsyncSession = Depends(get_db)):
    """
    🚀 YENİ ÜRÜN LANSMANI (COLD START)
    """
    # 1. Ürünü Ekle
    new_product = Product(
        name=product.name,
        category=product.category,
        cost=product.cost,
        price=product.price,
        abc_category="C" # Başlangıçta C
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    
    # 2. Tüm mağazalara dağıt (Başlangıç stoğu)
    result_stores = await db.execute(select(Store))
    stores = result_stores.scalars().all()
    
    for store in stores:
        inv = Inventory(
            store_id=store.id,
            product_id=new_product.id,
            quantity=product.initial_stock, # Lansman stoğu
            safety_stock=5
        )
        db.add(inv)
        
    await db.commit()
    
    # 3. Cold Start Tahmini Oluştur (Benzer ürünlere bakarak)
    # NOT: Bu kısım karmaşık analiz gerektirdiği için şimdilik async içinde
    # basit bir simülasyon yapıyoruz veya gelecekteki 'Analysis Engine'e devrediyoruz.
    
    return {"message": f"{new_product.name} lansmanı yapıldı ve mağazalara dağıtıldı.", "id": new_product.id}
