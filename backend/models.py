from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime
import enum

class StoreType(enum.Enum):
    CENTER = "CENTER" # Merkezi Depo
    HUB = "HUB"       # Ara Depo
    STORE = "STORE"   # Mağaza

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    store_type = Column(Enum(StoreType), default=StoreType.STORE)
    lat = Column(Float)
    lon = Column(Float)
    last_risk_analysis = Column(DateTime, nullable=True)
    
    # İlişkiler
    inventory = relationship("Inventory", back_populates="store")
    sales = relationship("Sale", back_populates="store")
    forecasts = relationship("Forecast", back_populates="store")
    features = relationship("StoreFeatures", back_populates="store", uselist=False)

class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=0)
    safety_stock = Column(Integer, default=10)

    store = relationship("Store", back_populates="inventory")
    product = relationship("Product")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, index=True, unique=True, nullable=True) # Barkod
    name = Column(String, index=True)
    category = Column(String, index=True)
    cost = Column(Float)
    price = Column(Float)
    abc_category = Column(String, default="C") # A, B, or C
    
    sales = relationship("Sale", back_populates="product")
    forecasts = relationship("Forecast", back_populates="product")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city = Column(String)
    phone = Column(String, unique=True, index=True, nullable=True) # Phase 8
    email = Column(String, nullable=True) # Phase 3 requirement
    
    # Loyalty Config (Phase 8)
    loyalty_score = Column(Float, default=0) # Legacy field
    points_balance = Column(Float, default=0.0)
    total_shopping_count = Column(Integer, default=0)

    # Marketing / Geofence (Phase 2)
    engagement_score = Column(Float, default=1.0) # Etkileşim Skoru
    interested_in_marketing = Column(Boolean, default=False) # Pazarlama İlgisi

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True) # Örn: KAR20
    customer_id = Column(Integer, ForeignKey("customers.id"))
    store_id = Column(Integer, ForeignKey("stores.id"))
    
    discount_amount = Column(Float) # İndirim tutarı veya oranı
    discount_type = Column(String, default="PERCENT") # PERCENT veya FIXED
    
    is_used = Column(Boolean, default=False)
    valid_until = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relations
    customer = relationship("Customer")
    store = relationship("Store")

class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    date = Column(Date, index=True)
    predicted_quantity = Column(Float) # Tahmin edilen satış adedi
    
    # Model Metadata (Opsiyonel)
    model_name = Column(String, default="SimpleRegression") # Hangi model kullanıldı?
    confidence_score = Column(Float, nullable=True) # Güven skoru
    
    # İlişkiler
    store = relationship("Store", back_populates="forecasts")
    product = relationship("Product", back_populates="forecasts")
    


# ==========================================
# 📊 Sales (Satış) Modeli - ANA TABLO
# ==========================================
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    date = Column(Date, index=True)
    quantity = Column(Integer) # Renamed from amount for consistency
    total_price = Column(Float) # Toplam tutar (amount * price) - Analiz için kritik
    
    # İlişkiler
    store = relationship("Store", back_populates="sales")
    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer")

    # --- OPTIMIZASYON ADAYLARI ---
    weather = Column(String) 
    holiday = Column(String) 
    promotion = Column(String)

# ==========================================
# 🔄 Transfers (Transferler) Modeli
# ==========================================
class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    source_store_id = Column(Integer, ForeignKey("stores.id")) # Nereden?
    target_store_id = Column(Integer, ForeignKey("stores.id")) # Nereye?
    product_id = Column(Integer, ForeignKey("products.id")) # Ne?
    amount = Column(Integer) # Kaç tane?
    status = Column(String, default="Pending") # "Pending", "Approved", "Completed"
    request_date = Column(DateTime, default=datetime.datetime.utcnow) # Talep tarihi
    
    # Transferin neden yapıldığı (Örn: "Stok Dengeleme", "Acil İhtiyaç")
    reason = Column(String, nullable=True)

# ==========================================
# 🌟 StoreFeatures (Mağaza Özellikleri)
# ==========================================
class StoreFeatures(Base):
    __tablename__ = "store_features"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    
    # Mağaza tipi (AVM, Cadde, vb.)
    store_type = Column(String) 
    
    # Çevresel faktörler (0-10 arası puanlar)
    competitor_density = Column(Float) # Rakip yoğunluğu
    population_density = Column(Float) # Nüfus yoğunluğu
    income_level = Column(Float) # Gelir seviyesi
    
    store = relationship("Store", back_populates="features")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) # Şimdilik plain text (Demo), normalde hashlenmeli
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    department = Column(String)
    role = Column(String, default="user") # admin, user
    calendar_url = Column(String, nullable=True) # Kişisel ICS Bağlantısı

class CalendarNote(Base):
    __tablename__ = "calendar_notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id")) # Notun sahibi
    date = Column(Date, index=True)
    time = Column(String, nullable=True) # Opsiyonel saat (HH:MM)
    title = Column(String)
    description = Column(String, nullable=True)
    color = Column(String, default="yellow") # yellow, blue, red, green
    created_at = Column(DateTime, default=datetime.datetime.now)

    user = relationship("User")

# ==========================================
# 🛑 Transfer Rejection & Penalty Modeli
# ==========================================
class TransferRejection(Base):
    __tablename__ = "transfer_rejections"

    id = Column(Integer, primary_key=True, index=True)
    source_store_id = Column(Integer, ForeignKey("stores.id"))
    target_store_id = Column(Integer, ForeignKey("stores.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    reason = Column(String) # COST, OPS, STRATEGY
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class RoutePenalty(Base):
    __tablename__ = "route_penalties"

    id = Column(Integer, primary_key=True, index=True)
    source_store_id = Column(Integer, ForeignKey("stores.id"))
    target_store_id = Column(Integer, ForeignKey("stores.id"))
    penalty_score = Column(Float, default=0.0) # Ceza puanı (Her reddedişte artar)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

# ==========================================
# 🛒 POS Staging Tables (Saha Operasyonları)
# ==========================================

from sqlalchemy import UniqueConstraint, JSON

class PosSale(Base):
    __tablename__ = "pos_sales"

    id = Column(Integer, primary_key=True, index=True)
    pos_device_id = Column(String, index=True) # Örn: POS-01
    receipt_no = Column(String, index=True) # Fiş No
    
    transaction_type = Column(String, default="SALE") # SALE, RETURN, VOID
    total_amount = Column(Float)
    currency = Column(String, default="TRY")
    
    status = Column(String, default="PENDING") # PENDING, PROCESSED, ERROR
    error_log = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # İlişkiler
    items = relationship("PosSaleItem", back_populates="sale", cascade="all, delete-orphan")
    payments = relationship("PosPayment", back_populates="sale", cascade="all, delete-orphan")

    # --- LOYALTY FIELDS (Phase 8) ---
    loyalty_points_earned = Column(Float, default=0.0)
    loyalty_points_used = Column(Float, default=0.0)

    __table_args__ = (
        UniqueConstraint('pos_device_id', 'receipt_no', name='uix_pos_receipt'),
    )

class PosSaleItem(Base):
    __tablename__ = "pos_sale_items"

    id = Column(Integer, primary_key=True, index=True)
    pos_sale_id = Column(Integer, ForeignKey("pos_sales.id"))
    
    product_sku = Column(String, index=True) # Barkod
    quantity = Column(Integer)
    unit_price = Column(Float)
    vat_rate = Column(Float, default=18.0) # KDV
    
    sale = relationship("PosSale", back_populates="items")

class PosPayment(Base):
    __tablename__ = "pos_payments"

    id = Column(Integer, primary_key=True, index=True)
    pos_sale_id = Column(Integer, ForeignKey("pos_sales.id"))
    
    payment_method = Column(String) # CASH, CREDIT_CARD, POINTS
    amount = Column(Float)

    sale = relationship("PosSale", back_populates="payments")

class PosZReport(Base):
    __tablename__ = "pos_z_reports"

    id = Column(Integer, primary_key=True, index=True)
    pos_device_id = Column(String, index=True)
    z_no = Column(String) # Z Raporu No
    date = Column(Date, index=True)
    
    total_sales = Column(Float)
    total_returns = Column(Float)
    total_cash = Column(Float)
    total_credit = Column(Float)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
