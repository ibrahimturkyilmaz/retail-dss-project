from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
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
    background_tasks.add_task(_send_welcome_email, new_customer.email, new_customer.name, new_customer.surname)
    
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

def _send_welcome_email(to_email: str, name: str, surname: str = None):
    """Background task: Yeni musteriye hos geldin maili gonder."""
    from services.email_service import send_z_report_email
    
    full_name = f"{name} {surname}" if surname else name
    first_letter = (name[0] if name else "R").upper()
    
    html_content = f"""<html><head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background-color:#0f0f23;font-family:'Segoe UI',Roboto,Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0f0f23;padding:30px 0;">
<tr><td align="center">
<table width="580" cellpadding="0" cellspacing="0" style="background:#1a1a2e;border-radius:24px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.5);">

<!-- HERO -->
<tr><td style="background:linear-gradient(135deg,#667eea 0%,#764ba2 50%,#f093fb 100%);padding:50px 40px;text-align:center;">
<div style="width:80px;height:80px;background:rgba(255,255,255,0.2);border-radius:20px;margin:0 auto 20px;line-height:80px;font-size:36px;color:#fff;font-weight:bold;">{first_letter}</div>
<h1 style="color:#fff;margin:0 0 8px;font-size:32px;font-weight:800;">Merhaba, {full_name}!</h1>
<p style="color:rgba(255,255,255,0.85);margin:0;font-size:16px;">StyleStore ailesine hosgeldiniz</p>
</td></tr>

<!-- WELCOME BADGE -->
<tr><td style="padding:30px 40px 10px;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:linear-gradient(135deg,#1e3a5f,#16213e);border-radius:16px;border:1px solid rgba(102,126,234,0.3);">
<tr>
<td style="padding:20px 24px;" width="60">
<div style="width:48px;height:48px;background:linear-gradient(135deg,#667eea,#764ba2);border-radius:14px;text-align:center;line-height:48px;font-size:22px;">&#127881;</div>
</td>
<td style="padding:20px 16px 20px 0;">
<p style="color:#667eea;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:2px;margin:0 0 4px;">Hos Geldin Bonusu</p>
<p style="color:#ffffff;font-size:22px;font-weight:800;margin:0;">100 Puan Hediye!</p>
</td>
</tr>
</table>
</td></tr>

<!-- FEATURES -->
<tr><td style="padding:20px 40px;">
<p style="color:rgba(255,255,255,0.5);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:3px;margin:0 0 16px;">Sizi Neler Bekliyor</p>
<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td width="33%" style="padding:8px 6px 8px 0;vertical-align:top;">
<div style="background:#16213e;border-radius:16px;padding:20px 14px;text-align:center;border:1px solid rgba(255,255,255,0.06);">
<div style="font-size:28px;margin-bottom:10px;">&#11088;</div>
<p style="color:#fff;font-size:13px;font-weight:700;margin:0 0 4px;">Sadakat Puanlari</p>
<p style="color:rgba(255,255,255,0.4);font-size:11px;margin:0;">Her alisveriste kazan</p>
</div>
</td>
<td width="33%" style="padding:8px 3px;vertical-align:top;">
<div style="background:#16213e;border-radius:16px;padding:20px 14px;text-align:center;border:1px solid rgba(255,255,255,0.06);">
<div style="font-size:28px;margin-bottom:10px;">&#127919;</div>
<p style="color:#fff;font-size:13px;font-weight:700;margin:0 0 4px;">Ozel Kampanyalar</p>
<p style="color:rgba(255,255,255,0.4);font-size:11px;margin:0;">Size ozel firsatlar</p>
</div>
</td>
<td width="33%" style="padding:8px 0 8px 6px;vertical-align:top;">
<div style="background:#16213e;border-radius:16px;padding:20px 14px;text-align:center;border:1px solid rgba(255,255,255,0.06);">
<div style="font-size:28px;margin-bottom:10px;">&#128205;</div>
<p style="color:#fff;font-size:13px;font-weight:700;margin:0 0 4px;">Yakin Magaza</p>
<p style="color:rgba(255,255,255,0.4);font-size:11px;margin:0;">Konuma ozel bildirim</p>
</div>
</td>
</tr>
</table>
</td></tr>

<!-- CTA -->
<tr><td style="padding:10px 40px 30px;text-align:center;">
<table cellpadding="0" cellspacing="0" style="margin:0 auto;">
<tr><td style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:14px;padding:16px 48px;">
<a href="#" style="color:#ffffff;text-decoration:none;font-size:15px;font-weight:700;letter-spacing:0.5px;">Alisverise Basla &#8594;</a>
</td></tr>
</table>
</td></tr>

<!-- FOOTER -->
<tr><td style="background:#12122a;padding:24px 40px;border-top:1px solid rgba(255,255,255,0.05);">
<table width="100%" cellpadding="0" cellspacing="0">
<tr>
<td><p style="color:rgba(255,255,255,0.25);font-size:11px;margin:0;">StyleStore by Retail DSS<br>Bu mail otomatik olarak gonderilmistir.</p></td>
<td align="right"><p style="color:rgba(255,255,255,0.15);font-size:10px;margin:0;">v1.3.0</p></td>
</tr>
</table>
</td></tr>

</table>
</td></tr>
</table>
</body></html>"""
    
    send_z_report_email(to_email, "Hosgeldiniz! StyleStore Ailesine Katildiniz", html_content)

