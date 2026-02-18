from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from typing import List

from database import get_db, get_sync_db
from models import Store, Inventory, Sale, RoutePenalty, TransferRejection, Product
from schemas import TransferRecommendationSchema, TransferRequest, RejectionRequest

# Imports from engines (Synchronous)
from transfer_engine import generate_transfer_recommendations

router = APIRouter(
    tags=["transfers"]
)

@router.get("/api/transfers/recommendations", response_model=List[TransferRecommendationSchema])
def get_transfer_recommendations(db: Session = Depends(get_sync_db)):
    """
    🚚 TRANSFER ÖNERİLERİ (ROBIN HOOD)
    NOT: Hesaplama motoru senkron olduğu için 'get_sync_db' kullanıyoruz.
    """
    stores = db.query(Store).all()
    recommendations = generate_transfer_recommendations(db, stores) 
    return recommendations

@router.post("/api/transfer")
async def transfer_stock(transfer_req: TransferRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """
    ⚡ TRANSFERİ GERÇEKLEŞTİR (AKSIYON) - ASYNC
    """
    # 1. Kaynak ve Hedef mağazayı bul
    res_source = await db.execute(select(Store).filter(Store.id == transfer_req.source_store_id))
    source = res_source.scalars().first()
    
    res_target = await db.execute(select(Store).filter(Store.id == transfer_req.target_store_id))
    target = res_target.scalars().first()
    
    if not source or not target:
        raise HTTPException(status_code=404, detail="Mağaza bulunamadı")
        
    # 2. Ürün bazlı stok kontrolü
    if transfer_req.product_id:
        res_source_item = await db.execute(select(Inventory).filter(Inventory.store_id == source.id, Inventory.product_id == transfer_req.product_id).options(selectinload(Inventory.product)))
        source_item = res_source_item.scalars().first()
        
        res_target_item = await db.execute(select(Inventory).filter(Inventory.store_id == target.id, Inventory.product_id == transfer_req.product_id))
        target_item = res_target_item.scalars().first()
        
        if not source_item:
             raise HTTPException(status_code=400, detail="Kaynak mağazada bu ürün yok")
             
        if not target_item:
            # Hedefte ürün yoksa oluştur (Sıfır stokla)
            target_item = Inventory(store_id=target.id, product_id=transfer_req.product_id, quantity=0, safety_stock=10) # safety default
            db.add(target_item)
            
        if source_item.quantity < transfer_req.amount:
            raise HTTPException(status_code=400, detail=f"Kaynak mağazada yetersiz stok (Mevcut: {source_item.quantity})")
            
        source_item.quantity -= transfer_req.amount
        target_item.quantity += transfer_req.amount
        
        product_name = source_item.product.name if source_item.product else "Ürün"
        msg = f"{source.name} şubesinden {target.name} şubesine {transfer_req.amount} adet {product_name} transfer edildi."

    else:
        raise HTTPException(status_code=400, detail="Transfer için product_id zorunludur.")
    
    await db.commit()
    return {"message": msg}

@router.post("/api/transfer/reject")
async def reject_transfer(request: RejectionRequest, db: AsyncSession = Depends(get_db)):
    """
    ❌ TRANSFER ÖNERİSİNİ REDDET - ASYNC
    """
    # 1. Red Kaydını Oluştur
    rejection = TransferRejection(
        source_store_id=request.source_store_id,
        target_store_id=request.target_store_id,
        product_id=request.product_id,
        reason=request.reason
    )
    db.add(rejection)
    
    # 2. Ceza Puanını Artır (Penalty)
    res_penalty = await db.execute(select(RoutePenalty).filter(
        RoutePenalty.source_store_id == request.source_store_id,
        RoutePenalty.target_store_id == request.target_store_id
    ))
    penalty = res_penalty.scalars().first()
    
    if not penalty:
        penalty = RoutePenalty(
            source_store_id=request.source_store_id,
            target_store_id=request.target_store_id,
            penalty_score=1
        )
        db.add(penalty)
    else:
        penalty.penalty_score += 1
        
    await db.commit()
    return {
        "message": "Transfer reddedildi ve rota cezalandırıldı.", 
        "new_penalty_score": penalty.penalty_score
    }
