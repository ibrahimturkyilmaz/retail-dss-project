from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
from models import User
from schemas import UserSchema, UserProfileUpdateSchema, UserSyncSchema
from core.logger import logger
from fastapi import BackgroundTasks
from core.email import send_welcome_email
import random

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.post("/sync", response_model=UserSchema)
async def sync_user(user_data: UserSyncSchema, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """
    🔄 Sync Supabase User with Backend & Trigger Welcome Email
    """
    # Check if user exists by email
    try:
        result = await db.execute(select(User).filter(User.email == user_data.email))
        user = result.scalars().first()

        if not user:
            logger.info(f"New User Sync: {user_data.email}")
            
            # Generate unique username
            base_username = user_data.username or user_data.email.split("@")[0]
            username = base_username
            
            # Simple collision check (try 3 times with random suffix)
            for _ in range(3):
                existing = await db.execute(select(User).filter(User.username == username))
                if not existing.scalars().first():
                    break
                username = f"{base_username}{random.randint(100, 999)}"
            
            user = User(
                username=username,
                email=user_data.email,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                department="Genel",
                role=user_data.role,
                password="oauth_user" # Placeholder
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)

            # Send Welcome Email
            background_tasks.add_task(send_welcome_email, user.email, user.first_name)
            logger.info(f"Welcome email queued for {user.email}")
        else:
            logger.info(f"User already exists: {user.email}")
        
        return user
    except Exception as e:
        logger.error(f"Sync error: {e}")
        raise HTTPException(status_code=500, detail="User sync failed")

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
