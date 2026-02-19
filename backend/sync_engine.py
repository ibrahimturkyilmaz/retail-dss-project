import logging
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from models import PosSale, Inventory, Product, Sale
from datetime import datetime

logger = logging.getLogger(__name__)

async def process_pending_sales(db: AsyncSession):
    """
    Bekleyen POS satışlarını işler ve ana envantere yansıtır.
    """
    # 1. Bekleyen satışları çek (Items ile birlikte)
    query = select(PosSale).options(selectinload(PosSale.items)).where(PosSale.status == "PENDING")
    result = await db.execute(query)
    pending_sales = result.scalars().all()
    
    if not pending_sales:
        return 0

    processed_count = 0
    
    for sale in pending_sales:
        try:
            await process_single_sale(db, sale)
            sale.status = "PROCESSED"
            processed_count += 1
        except Exception as e:
            logger.error(f"Error processing sale {sale.id}: {e}")
            sale.status = "ERROR"
            sale.error_log = str(e)
            # Hata durumunda rollback yapmıyoruz, sadece bu satışı ERROR işaretliyoruz
            # ve commit ediyoruz ki hata durumu kaydedilsin.
            
    await db.commit()
    return processed_count

async def process_single_sale(db: AsyncSession, pos_sale: PosSale):
    """
    Tek bir satışı işler:
    - Stok düş/arttır
    - Sale tablosuna kayıt at (Opsiyonel, raporlama için)
    """
    
    # Mağaza ID Belirleme (Şimdilik Mock veya Device ID'den)
    # Gerçek sistemde Device -> Store mapping tablosu olur.
    store_id = 1 # Varsayılan: Merkez Mağaza/Depo
    
    # Items Döngüsü
    for item in pos_sale.items:
        # Ürünü Bul (SKU ile)
        prod_query = select(Product).where(Product.sku == item.product_sku)
        prod_result = await db.execute(prod_query)
        product = prod_result.scalar_one_or_none()
        
        if not product:
            raise ValueError(f"Unknown SKU: {item.product_sku}")
        
        # Envanteri Bul
        inv_query = select(Inventory).where(
            Inventory.store_id == store_id,
            Inventory.product_id == product.id
        )
        inv_result = await db.execute(inv_query)
        inventory = inv_result.scalar_one_or_none()
        
        if not inventory:
            # Envanter kaydı yoksa oluştur? Veya hata ver?
            # Şimdilik hata verelim, ürün mağazada tanımlı olmalı.
            # Veya otomatik 0 stokla oluşturabiliriz.
            # raise ValueError(f"Product {product.name} not defined in store {store_id}")
            
            # Otomatik oluşturma (Daha esnek)
            inventory = Inventory(store_id=store_id, product_id=product.id, quantity=0)
            db.add(inventory)
        
        # Stok Güncelleme Mantığı
        qty_change = item.quantity
        
        if pos_sale.transaction_type == "SALE":
            inventory.quantity -= qty_change
        elif pos_sale.transaction_type == "RETURN":
            inventory.quantity += qty_change
        elif pos_sale.transaction_type == "VOID":
            pass # İşlem iptali, stok değişmez (veya loglanır)
            
        # Sale Tablosuna Kayıt (Opsiyonel Raporlama)
        # Gerçek Sale tablosuna da atalım ki dashboard çalışsın
        if pos_sale.transaction_type == "SALE":
             new_sale = Sale(
                 store_id=store_id,
                 product_id=product.id,
                 date=pos_sale.created_at.date() if pos_sale.created_at else datetime.utcnow().date(),
                 quantity=item.quantity,
                 total_price=item.quantity * item.unit_price
             )
             db.add(new_sale)

