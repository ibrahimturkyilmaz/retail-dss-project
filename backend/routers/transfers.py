from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Store, Inventory, Sale, RoutePenalty, TransferRejection
from schemas import TransferRecommendationSchema, TransferRequest, RejectionRequest

# Imports from engines (assuming they are available in PYTHONPATH)
from transfer_engine import generate_transfer_recommendations, calculate_distance
from slowapi import Limiter
from slowapi.util import get_remote_address

# Not: Global limiter'a erişim olmadığı için burada tekrar tanımlamak yerine
# dependency olarak alacağız veya pass geçeceğiz.
# Router seviyesinde limiter eklemek için main.py'deki limiter nesnesini 
# buraya taşımak en doğrusu olurdu.
# Şimdilik limiter'ı devre dışı bırakıyoruz (Refaktör önceliği).

router = APIRouter(
    tags=["transfers"]
)

@router.get("/api/transfers/recommendations", response_model=List[TransferRecommendationSchema])
def get_transfer_recommendations(db: Session = Depends(get_db)):
    """
    🚚 TRANSFER ÖNERİLERİ (ROBIN HOOD)
    """
    stores = db.query(Store).all()
    recommendations = generate_transfer_recommendations(db, stores) 
    return recommendations

@router.post("/api/transfer")
def transfer_stock(transfer_req: TransferRequest, request: Request, db: Session = Depends(get_db)):
    """
    ⚡ TRANSFERİ GERÇEKLEŞTİR (AKSIYON)
    """
    # 1. Kaynak ve Hedef mağazayı bul
    source = db.query(Store).filter(Store.id == transfer_req.source_store_id).first()
    target = db.query(Store).filter(Store.id == transfer_req.target_store_id).first()
    
    if not source or not target:
        raise HTTPException(status_code=404, detail="Mağaza bulunamadı")
        
    # 2. Ürün bazlı stok kontrolü
    if transfer_req.product_id:
        source_item = db.query(Inventory).filter(Inventory.store_id == source.id, Inventory.product_id == transfer_req.product_id).first()
        target_item = db.query(Inventory).filter(Inventory.store_id == target.id, Inventory.product_id == transfer_req.product_id).first()
        
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
        
        product_name = source_item.product.name
        msg = f"{source.name} şubesinden {target.name} şubesine {transfer_req.amount} adet {product_name} transfer edildi."

    else:
        raise HTTPException(status_code=400, detail="Transfer için product_id zorunludur.")
    
    db.commit()
    return {"message": msg}

@router.post("/api/transfer/reject")
def reject_transfer(request: RejectionRequest, db: Session = Depends(get_db)):
    """
    ❌ TRANSFER ÖNERİSİNİ REDDET
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
    penalty = db.query(RoutePenalty).filter(
        RoutePenalty.source_store_id == request.source_store_id,
        RoutePenalty.target_store_id == request.target_store_id
    ).first()
    
    if not penalty:
        penalty = RoutePenalty(
            source_store_id=request.source_store_id,
            target_store_id=request.target_store_id,
            penalty_score=1
        )
        db.add(penalty)
    else:
        penalty.penalty_score += 1
        
    db.commit()
    return {
        "message": "Transfer reddedildi ve rota cezalandırıldı.", 
        "new_penalty_score": penalty.penalty_score
    }
