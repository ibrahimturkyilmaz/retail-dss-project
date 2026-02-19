import logging
import random
import datetime
import google.generativeai as genai
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from core.config import settings
from models import Customer, Coupon, Store, Sale, Product
from services.weather_service import get_current_weather

logger = logging.getLogger(__name__)

# Configure Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

async def analyze_customer_context(db: AsyncSession, customer_id: int, store_id: int, lat: float, lon: float):
    """
    Analyzes customer, store, weather, and sales trends to build a marketing context.
    """
    # 1. Customer Info
    res_customer = await db.execute(select(Customer).filter(Customer.id == customer_id))
    customer = res_customer.scalars().first()
    if not customer:
        return None

    # 2. Store Info
    res_store = await db.execute(select(Store).filter(Store.id == store_id))
    store = res_store.scalars().first()
    if not store:
        return None

    # 3. Weather (Current)
    # Service uses sync requests, so just call it (blocking but fast enough for now, or wrap in run_in_executor)
    weather = get_current_weather(f"{lat},{lon}")
    weather_desc = "Bilinmiyor"
    temp = 20
    if weather:
        weather_desc = weather.get("condition", "Normal")
        temp = weather.get("temp_c", 20)

    # 4. Best Selling Product (Contextual)
    # Simple logic: If cold -> Hot drinks/clothes, If hot -> Cold drinks
    # For now, we query top selling product in that store
    # Complex join query
    stmt = (
        select(Product)
        .join(Sale)
        .filter(Sale.store_id == store_id)
        .group_by(Product.id)
        .order_by(func.sum(Sale.quantity).desc())
        .limit(1)
    )
    res_product = await db.execute(stmt)
    top_product = res_product.scalars().first()
    
    product_name = top_product.name if top_product else "Sürpriz Ürün"

    return {
        "customer_name": customer.name,
        "points": customer.points_balance,
        "store_name": store.name,
        "weather_condition": weather_desc,
        "temperature": temp,
        "product_recommendation": product_name
    }

def generate_smart_message(context: dict):
    """
    Uses Gemini to generate a personalized push notification message.
    """
    # Fallback if no API key
    if not settings.GEMINI_API_KEY:
        return {
            "title": f"Merhaba {context['customer_name']}!",
            "message": f"{context['store_name']} mağazasına hoş geldin! {context['points']} puanın var."
        }
        
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = (
            f"Bir perakende mağazası için kısa bir 'Push Notification' mesajı yaz.\n"
            f"Müşteri: {context['customer_name']}\n"
            f"Mağaza: {context['store_name']}\n"
            f"Hava Durumu: {context['weather_condition']} ({context['temperature']}°C)\n"
            f"Önerilen Ürün: {context['product_recommendation']}\n"
            f"Puan Bakiyesi: {context['points']}\n"
            f"Kısıt: Samimi ol, aciliyet hissi yarat, emojiler kullan. En fazla 2 cümle."
        )
        # Gemini call is sync, strictly speaking should be async or threadpool, but keeping sync for simplicity in demo
        response = model.generate_content(prompt)
        text = response.text.replace("\n", " ").strip()
        
        return {
            "title": f"👋 {context['customer_name']}, Bi' Bakar Mısın?",
            "message": text
        }
    except Exception as e:
        logger.error(f"Gemini Error: {e}")
        return {
             "title": "Fırsatı Kaçırma!",
             "message": f"Hava {context['temperature']}°C! {context['product_recommendation']} seni bekliyor."
        }

async def create_coupon(db: AsyncSession, customer_id: int, store_id: int):
    """
    Generates a unique coupon code valid for 2 hours.
    """
    code = f"FIRSAT-{datetime.datetime.now().strftime('%M%S')}-{random.randint(10,99)}"
    
    valid_until = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    
    coupon = Coupon(
        code=code,
        customer_id=customer_id,
        store_id=store_id,
        discount_amount=20.0, # %20 or 20 TL logic needs defining
        discount_type="PERCENT",
        is_used=False,
        valid_until=valid_until
    )
    db.add(coupon)
    await db.commit()
    await db.refresh(coupon)
    return coupon
