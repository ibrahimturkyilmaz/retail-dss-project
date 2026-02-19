from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
import datetime

# --- Base Models ---

class StoreSchema(BaseModel):
    id: int
    name: str
    store_type: str # Enum string olarak dönecek
    lat: float
    lon: float
    stock: int
    safety_stock: int
    risk_status: str

    class Config:
        from_attributes = True

class ProductSchema(BaseModel):
    id: int
    name: str
    category: str
    price: float
    abc_category: Optional[str]

    class Config:
        from_attributes = True

class TransferRequest(BaseModel):
    source_store_id: int
    target_store_id: int
    product_id: int
    amount: int

class AnalyticsResponse(BaseModel):
    total_revenue: float
    top_selling_product: str
    total_transactions: int

class SaleSchema(BaseModel):
    id: int
    store_name: str
    product_name: str
    customer_name: str
    date: datetime.date
    quantity: int
    total_price: float

    class Config:
        from_attributes = True

# --- Transfer Engine Schemas ---
class XaiExplanationSchema(BaseModel):
    summary: str
    reasons: List[str]
    score: int
    type: str

class StoreInfoSchema(BaseModel):
    id: int
    name: str
    type: str

class TransferRecommendationSchema(BaseModel):
    transfer_id: str
    source: StoreInfoSchema
    target: StoreInfoSchema
    product_id: int
    product: str
    amount: int
    xai_explanation: XaiExplanationSchema
    algorithm: str

# --- User Schemas ---
class UserSchema(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    department: str
    role: str
    calendar_url: Optional[str] = None

    class Config:
        from_attributes = True

class UserProfileUpdateSchema(BaseModel):
    email: str
    first_name: str
    last_name: str
    department: str
    calendar_url: Optional[str] = None
    password: Optional[str] = None 

class UserSyncSchema(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: Optional[str] = None
    role: str = "user" 

# --- Inventory Schemas ---
class InventorySchema(BaseModel):
    product_id: int
    product_name: str
    category: str
    quantity: int
    safety_stock: int
    abc_category: str
    forecast_next_7_days: float

# --- Simulation Schemas ---
class SimulationStats(BaseModel):
    total_revenue: float
    total_stock: int
    critical_stores: int

class CustomScenarioRequest(BaseModel):
    price_change: int
    delay_days: int

class NearbyStoreRequest(BaseModel):
    lat: float
    lon: float

class WhatIfRequest(BaseModel):
    source_store_id: int
    target_store_id: int
    product_id: int
    amount: int

class RejectionRequest(BaseModel):
    transfer_id: str 
    source_store_id: int
    target_store_id: int
    product_id: int
    reason: str 

class NewProductSchema(BaseModel):
    name: str
    category: str
    price: float
    cost: float
    reference_product_id: int = None

# --- Calendar Schemas ---
class CalendarNoteSchema(BaseModel):
    id: int
    date: datetime.date
    time: Optional[str] = None
    title: str
    description: Optional[str] = None
    color: str = "yellow"
    
    class Config:
        from_attributes = True

class NoteCreateSchema(BaseModel):
    date: datetime.date
    time: Optional[str] = None
    title: str
    description: Optional[str] = None
    color: str = "yellow"
    username: str 

# --- SQL Playground ---
class SQLQueryRequest(BaseModel):
    query: str

class GenerateSQLRequest(BaseModel):
    prompt: str

class SQLQueryResponse(BaseModel):
    columns: List[str]
    data: List[dict]
    row_count: int
    execution_time_ms: float

# --- AI Chat ---
class AIChatRequest(BaseModel):
    message: str
    history: list = []
    voice_gender: str = "female"
    
# --- POS Schemas ---
class PosSaleItemBase(BaseModel):
    product_sku: str
    quantity: int
    unit_price: float
    vat_rate: float = 18.0

class PosPaymentBase(BaseModel):
    payment_method: str
    amount: float

class PosSaleCreate(BaseModel):
    pos_device_id: str
    receipt_no: str
    transaction_type: str = "SALE"
    total_amount: float
    currency: str = "TRY"
    items: List[PosSaleItemBase]
    payments: List[PosPaymentBase]
    created_at: Optional[datetime.datetime] = None

class PosSaleResponse(BaseModel):
    id: int
    pos_device_id: str
    receipt_no: str
    status: str
    total_amount: float
    created_at: datetime.datetime
    
    class Config:
        from_attributes = True

class PosZReportCreate(BaseModel):
    pos_device_id: str
    z_no: str
    total_sales: float
    total_returns: float
    total_cash: float
    total_credit: float
    date: datetime.date

