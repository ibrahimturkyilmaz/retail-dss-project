from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Customer
from pydantic import BaseModel
from typing import Optional, List

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
    phone: Optional[str]
    email: Optional[str]
    points_balance: float
    total_shopping_count: int

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

@router.post("/mobile-login", response_model=CustomerResponse)
async def mobile_login(data: dict, db: AsyncSession = Depends(get_db)):
    """
    Mobile for Mobile App: Login or Register with Email.
    Returns existing customer if email exists, else creates new one.
    """
    email = data.get("email")
    name = data.get("name", "Mobil Kullanıcı")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
        
    # Check if customer exists by email
    result = await db.execute(select(Customer).where(Customer.email == email))
    existing_customer = result.scalar_one_or_none()
    
    if existing_customer:
        return existing_customer
        
    # If not exists, create new
    # Generate a dummy phone if needed or make it nullable in DB (it is nullable in model)
    new_customer = Customer(
        name=name,
        email=email,
        phone=None, # Opsiyonel
        city="Mobil",
        points_balance=0,
        total_shopping_count=0
    )
    
    db.add(new_customer)
    await db.commit()
    await db.refresh(new_customer)
    return new_customer

@router.get("/search", response_model=List[CustomerResponse])
async def search_customers(q: str, db: AsyncSession = Depends(get_db)):
    """
    İsim veya Telefon ile arama yapar.
    """
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
