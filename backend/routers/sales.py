from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List

from database import get_db
from models import Sale, Store, Product, Customer
from schemas import SaleSchema

router = APIRouter(
    prefix="/api/sales",
    tags=["sales"]
)

@router.get("", response_model=List[SaleSchema])
async def read_sales(request: Request, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    💰 SATIŞ VERİLERİNİ LİSTELE
    Async + Eager Loading (Joined Load) ile optimize edildi.
    """
    # N+1 sorununu önlemek için select ile join yapabiliriz veya lazy load kullanabiliriz.
    # AsyncSession lazy load'u varsayılan olarak desteklemez (awaitable attributes gerekir).
    # Bu yüzden `select(Sale).options(selectinload(Sale.store))` vb. kullanmak en iyisidir.
    # Ancak basitlik için şimdilik scalar() ve hybrid property/lazy="selectin" kullanıyor olabiliriz.
    # Model tanımlarını görmedim, varsayılan olarak lazy='select' ise async'de hata verir.
    # Çözüm: Modellerde lazy='selectin' veya eager loading.
    # Şimdilik basic select yapalım, hata alırsak lazy option ekleriz.
    
    from sqlalchemy.orm import selectinload
    stmt = select(Sale).options(
        selectinload(Sale.store),
        selectinload(Sale.product),
        selectinload(Sale.customer)
    ).order_by(Sale.date.desc()).offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    sales = result.scalars().all()
    
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
