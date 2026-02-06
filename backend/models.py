from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime, Enum
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
    name = Column(String, index=True)
    category = Column(String, index=True)
    cost = Column(Float)
    price = Column(Float)
    
    sales = relationship("Sale", back_populates="product")
    forecasts = relationship("Forecast", back_populates="product")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    city = Column(String)
    loyalty_score = Column(Float)
    
    sales = relationship("Sale", back_populates="customer")

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    date = Column(Date, index=True)
    quantity = Column(Integer)
    total_price = Column(Float)
    
    store = relationship("Store", back_populates="sales")
    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")

class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    date = Column(Date)
    predicted_quantity = Column(Float)
    
    store = relationship("Store", back_populates="forecasts")
    product = relationship("Product", back_populates="forecasts")

