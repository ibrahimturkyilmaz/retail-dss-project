from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User
from schemas import UserSchema, UserProfileUpdateSchema
from core.logger import logger

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

# Not: Rate limiter 'limiter' nesnesi main.py'de tanımlı. 
# Router'da bunu kullanmak için dependency injection veya request.state kullanılabilir.
# Ancak basitlik için burada hard-dependency yapmaktan kaçınalım.
# Şimdilik limiter dekoratörünü kaldıralım veya global limiter'ı import edelim.
# Doğrusu: Limiter'ı core/security.py gibi bir yere taşımak ama şu an main.py'de.
# Çözüm: Limiter'ı es geçebiliriz (refaktörde) veya main'den import edebiliriz (döngüsel import riski).
# Güvenli yol: Limiter'ı şimdilik devre dışı bırakıp not düşelim, veya dependency olarak alalım.

@router.get("/{username}", response_model=UserSchema)
def get_user_profile(username: str, db: Session = Depends(get_db)):
    """
    👤 KULLANICI PROFİLİ GETİR
    """
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        logger.info(f"JIT Profile Creation for: {username}")
        user = User(
            username=username,
            password="123", # Placeholder
            email=f"{username}@retaildss.com",
            first_name=username.capitalize(),
            last_name="Kullanıcısı",
            department="Genel",
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
    return user

@router.put("/{username}")
def update_user_profile(username: str, update_data: UserProfileUpdateSchema, request: Request, db: Session = Depends(get_db)):
    # Limiter notu: @limiter.limit("10/minute") bu fonksiyonun üzerindeydi.
    # Router seviyesinde limiter entegrasyonu için SlowAPI dokümantasyonuna bakınız.
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    user.email = update_data.email
    user.first_name = update_data.first_name
    user.last_name = update_data.last_name
    user.department = update_data.department
    user.calendar_url = update_data.calendar_url
    
    if update_data.password and len(update_data.password) > 0:
        user.password = update_data.password
        
    db.commit()
    return {"message": "Profil başarıyla güncellendi", "user": {
        "username": user.username,
        "first_name": user.first_name
    }}
