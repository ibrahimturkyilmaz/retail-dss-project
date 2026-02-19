from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Customer
from pydantic import BaseModel
from typing import Optional, List
from core.logger import logger

router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"],
    responses={404: {"description": "Not found"}},
)

class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    city: Optional[str] = None

class CustomerResponse(BaseModel):
    id: int
    name: str
    surname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None
    email_verified: bool = False
    points_balance: float
    total_shopping_count: int

class MobileLoginResponse(BaseModel):
    id: int
    name: str
    surname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None
    email_verified: bool = False
    points_balance: float
    total_shopping_count: int
    is_new_user: bool = False

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None

@router.post("/", response_model=CustomerResponse)
async def create_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    # Check existing phone
    result = await db.execute(select(Customer).where(Customer.phone == customer.phone))
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail="Bu telefon numarası ile kayıtlı müşteri var.")
        
    new_customer = Customer(
        name=customer.name,
        phone=customer.phone,
        email=customer.email,
        city=customer.city,
        points_balance=0,
        total_shopping_count=0
    )
    
    db.add(new_customer)
    await db.commit()
    await db.refresh(new_customer)
    return new_customer

@router.post("/mobile-login", response_model=MobileLoginResponse)
async def mobile_login(data: dict, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """
    Mobile App: Login or Register with Email.
    Returns existing customer if email exists, else creates new one.
    Sends welcome email on first registration.
    """
    email = data.get("email")
    name = data.get("name", "Mobil Kullanıcı")
    surname = data.get("surname")
    photo_url = data.get("photo")  # Google photo URL
    
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    # Auto-split name if surname not provided (e.g. from Google: "Merve Yılmaz")
    if not surname and name and " " in name:
        parts = name.split(" ", 1)
        name = parts[0]
        surname = parts[1]
        
    # Check if customer exists by email
    result = await db.execute(select(Customer).where(Customer.email == email))
    existing_customer = result.scalar_one_or_none()
    
    if existing_customer:
        # Update photo if provided (Google may have updated it)
        if photo_url and not existing_customer.photo_url:
            existing_customer.photo_url = photo_url
            await db.commit()
            await db.refresh(existing_customer)
        
        return MobileLoginResponse(
            id=existing_customer.id,
            name=existing_customer.name,
            surname=existing_customer.surname,
            phone=existing_customer.phone,
            email=existing_customer.email,
            photo_url=existing_customer.photo_url or photo_url,
            email_verified=existing_customer.email_verified,
            points_balance=existing_customer.points_balance,
            total_shopping_count=existing_customer.total_shopping_count,
            is_new_user=False
        )
        
    # If not exists, create new customer
    new_customer = Customer(
        name=name,
        surname=surname,
        email=email,
        phone=None,
        photo_url=photo_url,
        email_verified=True,  # Otomatik doğrulanmış
        city="Mobil",
        points_balance=0,
        total_shopping_count=0,
        interested_in_marketing=True
    )
    
    db.add(new_customer)
    await db.commit()
    await db.refresh(new_customer)
    
    # Send welcome email in background
    logger.info(f"🆕 New Customer Created: {new_customer.email}. Queuing welcome email...")
    from core.email import send_welcome_email_customer
    background_tasks.add_task(send_welcome_email_customer, new_customer.email, new_customer.name)
    logger.info(f"📧 Background task added for {new_customer.email}")
    
    return MobileLoginResponse(
        id=new_customer.id,
        name=new_customer.name,
        surname=new_customer.surname,
        phone=new_customer.phone,
        email=new_customer.email,
        photo_url=new_customer.photo_url,
        email_verified=new_customer.email_verified,
        points_balance=new_customer.points_balance,
        total_shopping_count=new_customer.total_shopping_count,
        is_new_user=True
    )

@router.put("/{customer_id}/profile", response_model=CustomerResponse)
async def update_profile(customer_id: int, data: ProfileUpdate, db: AsyncSession = Depends(get_db)):
    """Müşteri profilini güncelle."""
    result = await db.execute(select(Customer).filter(Customer.id == customer_id))
    customer = result.scalars().first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    
    if data.name is not None:
        customer.name = data.name
    if data.surname is not None:
        customer.surname = data.surname
    if data.phone is not None:
        customer.phone = data.phone
    if data.photo_url is not None:
        customer.photo_url = data.photo_url
        
    await db.commit()
    await db.refresh(customer)
    return customer

@router.get("/search", response_model=List[CustomerResponse])
async def search_customers(q: str, db: AsyncSession = Depends(get_db)):
    """İsim veya Telefon ile arama yapar."""
    query = select(Customer).where(
        (Customer.phone.contains(q)) | (Customer.name.ilike(f"%{q}%"))
    )
    result = await db.execute(query)
    customers = result.scalars().all()
    return customers

class UpdatePreferences(BaseModel):
    interested_in_marketing: bool

@router.put("/{customer_id}/preferences")
async def update_preferences(customer_id: int, prefs: UpdatePreferences, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).filter(Customer.id == customer_id))
    customer = result.scalars().first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
        
    customer.interested_in_marketing = prefs.interested_in_marketing
    await db.commit()
    
    return {"status": "success", "interested_in_marketing": customer.interested_in_marketing}


# Local _send_welcome_email removed. Use core.email.send_welcome_email_customer instead.
