from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List

from database import get_db
from models import Sale
from schemas import SaleSchema

router = APIRouter(
    prefix="/api/sales",
    tags=["sales"]
)

# Not: Rate limiter main.py'de kaldığı için burada dekoratör kullanmıyoruz.
# İleride global limiter eklenebilir.

@router.get("", response_model=List[SaleSchema])
def read_sales(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    💰 SATIŞ VERİLERİNİ LİSTELE
    
    Tüm mağazaların satış geçmişini tarih sırasına göre (en yeniden eskiye) getirir.
    Pagination (Sayfalama) destekler: skip=atla, limit=getir.
    """
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
