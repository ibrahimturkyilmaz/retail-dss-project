from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
from models import User
from schemas import UserSchema, UserProfileUpdateSchema
from core.logger import logger
from fastapi import BackgroundTasks
from core.email import send_welcome_email

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.get("/{username}", response_model=UserSchema)
async def get_user_profile(username: str, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """
    👤 KULLANICI PROFİLİ GETİR
    """
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    
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
        await db.commit()
        await db.refresh(user)

        # Send Automatic Welcome Email (Background Task)
        background_tasks.add_task(send_welcome_email, user.email, user.first_name)
        logger.info(f"Queued welcome email for {user.email}")
        
    return user

@router.put("/{username}")
async def update_user_profile(username: str, update_data: UserProfileUpdateSchema, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    user.email = update_data.email
    user.first_name = update_data.first_name
    user.last_name = update_data.last_name
    user.department = update_data.department
    user.calendar_url = update_data.calendar_url
    
    if update_data.password and len(update_data.password) > 0:
        user.password = update_data.password
        
    await db.commit()
    return {"message": "Profil başarıyla güncellendi", "user": {
        "username": user.username,
        "first_name": user.first_name
    }}
