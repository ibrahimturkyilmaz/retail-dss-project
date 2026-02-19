from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from database import get_db
from models import Customer, Store, Coupon
from services.marketing_service import analyze_customer_context, generate_smart_message, create_coupon
from services.email_service import send_marketing_email
import logging
from math import radians, sin, cos, sqrt, atan2

router = APIRouter(tags=["marketing"])
logger = logging.getLogger(__name__)

class LocationCheck(BaseModel):
    lat: float
    lon: float
    customer_id: int  # In a real app, this comes from Auth token

# Haversine Formula for distance
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000 # Earth radius in meters
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

@router.post("/api/marketing/check-proximity")
async def check_proximity(data: LocationCheck, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """
    Checks if user is near a store. If yes, triggers marketing flow.
    """
    # 1. Find nearest store (< 500m)
    res_stores = await db.execute(select(Store))
    stores = res_stores.scalars().all()
    
    nearest_store = None
    min_dist = float('inf')
    
    for store in stores:
        if store.lat and store.lon:
            dist = calculate_distance(data.lat, data.lon, store.lat, store.lon)
            if dist < 500: # 500 meters geofence
                nearest_store = store
                min_dist = dist
                break
    
    if not nearest_store:
        return {"notification": False, "reason": "No store nearby"}

    # 3. Analyze Context & Generate Content
    # Service functions are now async and take AsyncSession
    context = await analyze_customer_context(db, data.customer_id, nearest_store.id, data.lat, data.lon)
    if not context:
        return {"notification": False, "reason": "Context analysis failed"}
        
    # 4. Generate Message (Gemini)
    content = generate_smart_message(context)
    
    # 5. Create Coupon
    coupon = await create_coupon(db, data.customer_id, nearest_store.id)
    
    # 6. Send Email (Background Task)
    # Query email async
    res_email = await db.execute(select(Customer.email).filter(Customer.id == data.customer_id))
    customer_email = res_email.scalar()
    
    if customer_email:
        background_tasks.add_task(
            send_marketing_email, 
            customer_email, 
            content["title"], 
            {**context, "message": content["message"]}, 
            coupon.code
        )
    
    # 7. Return Notification Data to App
    return {
        "notification": True,
        "title": content["title"],
        "message": content["message"],
        "store": nearest_store.name,
        "distance": int(min_dist),
        "coupon_code": coupon.code
    }

class CouponRedeem(BaseModel):
    code: str

@router.post("/api/marketing/redeem-coupon")
async def redeem_coupon(data: CouponRedeem, db: AsyncSession = Depends(get_db)):
    res_coupon = await db.execute(select(Coupon).filter(Coupon.code == data.code))
    coupon = res_coupon.scalars().first()
    
    if not coupon:
        raise HTTPException(status_code=404, detail="Kupon bulunamadı")
        
    if coupon.is_used:
        raise HTTPException(status_code=400, detail="Kupon zaten kullanılmış")
        
    # Mark as used
    coupon.is_used = True
    
    # Update Customer Engagement
    res_customer = await db.execute(select(Customer).filter(Customer.id == coupon.customer_id))
    customer = res_customer.scalars().first()
    
    if customer:
        customer.engagement_score += 10
        customer.interested_in_marketing = True
        customer.points_balance += 5 # Bonus points for using coupon
        
    await db.commit()
    
    return {"status": "success", "message": "Kupon doğrulandı", "discount": coupon.discount_amount}
