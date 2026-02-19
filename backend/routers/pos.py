from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List
from database import get_db
from models import PosSale, PosSaleItem, PosPayment, PosZReport
from schemas import PosSaleCreate, PosSaleResponse, PosZReportCreate
from services.email_service import send_z_report_email
from services.receipt_service import process_receipt_delivery

router = APIRouter(
    prefix="/api/pos",
    tags=["POS Integration"],
    responses={404: {"description": "Not found"}},
)

@router.post("/sync", response_model=PosSaleResponse)
async def sync_pos_sale(
    sale_data: PosSaleCreate, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    POS cihazından gelen satış verisini karşılar.
    Idempotency: Aynı (device_id + receipt_no) gelirse hata fırlatır.
    """
    # 1. Idempotency Check
    query = select(PosSale).where(
        PosSale.pos_device_id == sale_data.pos_device_id,
        PosSale.receipt_no == sale_data.receipt_no
    )
    result = await db.execute(query)
    existing_sale = result.scalar_one_or_none()
    
    if existing_sale:
        # Eğer zaten varsa, mevcut kaydı dön (Idempotent response)
        # Veya 409 Conflict dönebiliriz, ama POS genelde 200 OK bekler.
        return existing_sale

    try:
        # 2. Create Sale Header
        new_sale = PosSale(
            pos_device_id=sale_data.pos_device_id,
            receipt_no=sale_data.receipt_no,
            transaction_type=sale_data.transaction_type,
            total_amount=sale_data.total_amount,
            currency=sale_data.currency,
            status="PENDING",
            created_at=sale_data.created_at
        )
        db.add(new_sale)
        await db.flush() # ID almak için flush

        # 3. Create Items
        for item in sale_data.items:
            db_item = PosSaleItem(
                pos_sale_id=new_sale.id,
                product_sku=item.product_sku,
                quantity=item.quantity,
                unit_price=item.unit_price,
                vat_rate=item.vat_rate
            )
            db.add(db_item)

        # 4. Create Payments
        for payment in sale_data.payments:
            db_payment = PosPayment(
                pos_sale_id=new_sale.id,
                payment_method=payment.payment_method,
                amount=payment.amount
            )
            db.add(db_payment)

        await db.commit()
        await db.refresh(new_sale)
        
        # 5. Trigger Processing (Phase 3)
        # background_tasks.add_task(process_pos_sale, new_sale.id)
        
        return new_sale

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Database integrity error")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/z-report")
async def create_z_report(
    report_request: PosZReportCreate,
    email: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Gün Sonu (Z-Raporu) oluşturur ve e-posta gönderir.
    """
    try:
        # 1. DB'ye Kaydet
        z_report = PosZReport(
            pos_device_id=report_request.pos_device_id,
            z_no=report_request.z_no,
            date=report_request.date,
            total_sales=report_request.total_sales,
            total_returns=report_request.total_returns,
            total_cash=report_request.total_cash,
            total_credit=report_request.total_credit,
            created_at=datetime.datetime.now()
        )
        db.add(z_report)
        await db.commit()
        await db.refresh(z_report)

        # 2. Email İçeriği Hazırla
        subject = f"Z-Raporu: {report_request.date} - {report_request.pos_device_id}"
        body_html = f"""
        <html>
            <body>
                <h2>Gün Sonu Raporu (Z-Raporu)</h2>
                <p><strong>Tarih:</strong> {report_request.date}</p>
                <p><strong>Cihaz:</strong> {report_request.pos_device_id}</p>
                <p><strong>Z-No:</strong> {report_request.z_no}</p>
                <hr>
                <h3>Özet</h3>
                <ul>
                    <li><strong>Toplam Satış:</strong> {report_request.total_sales} TL</li>
                    <li><strong>İadeler:</strong> {report_request.total_returns} TL</li>
                    <li><strong>Nakit Ciro:</strong> {report_request.total_cash} TL</li>
                    <li><strong>Kredi Kartı:</strong> {report_request.total_credit} TL</li>
                </ul>
                <p><em>Bu e-posta RetailDSS sistemi tarafından otomatik oluşturulmuştur.</em></p>
            </body>
        </html>
        """
        
        # 3. Arka Planda Gönder
        background_tasks.add_task(send_z_report_email, email, subject, body_html)
        
        return {"message": "Z-Raporu oluşturuldu ve e-posta kuyruğuna eklendi.", "id": z_report.id}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/random")
async def get_random_product(db: AsyncSession = Depends(get_db)):
    """
    Simülasyon için rastgele bir ürün döner.
    """
    import random
    from models import Product  # Import here to avoid circular or top-level mess if not imported
    query = select(Product)
    result = await db.execute(query)
    products = result.scalars().all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    
    product = random.choice(products)
    return {
        "id": product.id,
        "sku": product.sku,
        "name": product.name,
        "price": product.price,
        "category": product.category
    }
@router.get("/products/scan/{barcode}")
async def scan_product(barcode: str, db: AsyncSession = Depends(get_db)):
    """
    Barkod ile ürün arama.
    """
    from models import Product
    # Remove leading zeros if any, though our script generated solid strings.
    # Handle bothexact match.
    query = select(Product).where(Product.sku == barcode)
    result = await db.execute(query)
    product = result.scalar_one_or_none()
    
    if not product:
         raise HTTPException(status_code=404, detail="Ürün bulunamadı")
         
    return {
        "id": product.id,
        "sku": product.sku,
        "name": product.name,
        "price": product.price,
        "category": product.category
    }

@router.post("/sales")
async def create_pos_sale_direct(
    sale_data: PosSaleCreate,
    email: str = None,
    customer_id: int = None, # Added for loyalty
    background_tasks: BackgroundTasks = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Saha satışı (Online). 
    1. Kaydı oluştur.
    2. Stok düş (ID: 9999).
    3. Sadakat Puanı Hesapla & Güncelle.
    4. PDF Fiş üret ve mail at.
    """
    from models import Inventory, Product # Local import
    
    try:
        new_sale = PosSale(
            pos_device_id=sale_data.pos_device_id,
            receipt_no=sale_data.receipt_no,
            transaction_type="SALE",
            total_amount=sale_data.total_amount,
            status="PROCESSED", # Direct processing
            created_at=sale_data.created_at or datetime.datetime.now()
        )
        db.add(new_sale)
        await db.flush()

        # Items & Stock Update (Store 9999)
        field_store_id = 9999
        
        for item in sale_data.items:
            # Item Kaydı
            db_item = PosSaleItem(
                pos_sale_id=new_sale.id,
                product_sku=item.product_sku,
                quantity=item.quantity,
                unit_price=item.unit_price
            )
            db.add(db_item)
            
            # Stok Düşümü (Field Store)
            # Find Product ID by SKU
            prod_res = await db.execute(select(Product).where(Product.sku == item.product_sku))
            product = prod_res.scalar_one_or_none()
            
            if product:
                inv_res = await db.execute(select(Inventory).where(
                    Inventory.store_id == field_store_id,
                    Inventory.product_id == product.id
                ))
                inventory = inv_res.scalar_one_or_none()
                
                if inventory:
                    inventory.quantity -= item.quantity
                    db.add(inventory) # Update
                else:
                    # Create negative stock or handle error? 
                    # For field ops, maybe allow negative or create 0
                    pass 

        # 6. Loyalty Program (Phase 8)
        from models import Customer
        from services.loyalty_service import calculate_loyalty_points
        
        final_customer_id = None
        points_earned = 0
        points_used = 0
        customer = None
        
        # Priority: customer_id > email
        if customer_id:
             cust_res = await db.execute(select(Customer).where(Customer.id == customer_id))
             customer = cust_res.scalar_one_or_none()
        elif email:
            # Fallback find customer by email
            cust_res = await db.execute(select(Customer).where(Customer.email == email))
            customer = cust_res.scalar_one_or_none()
            
        if customer:
            final_customer_id = customer.id
            
            # --- Check Payments for Points Usage ---
            for payment in sale_data.payments:
                if payment.payment_method == "POINTS":
                    points_to_use = payment.amount
                    if customer.points_balance < points_to_use:
                         raise HTTPException(status_code=400, detail="Yetersiz Puan Bakiyesi")
                    
                    customer.points_balance -= points_to_use
                    points_used += points_to_use
            
            # 1. Increment Shopping Count for this new sale
            customer.total_shopping_count += 1
            
            # 2. Calculate Earned Points (Net Tutar Üzerinden mi? Genelde Toplam Tutar)
            # Eğer puanla ödenen kısımdan puan kazanılmasın isteniyorsa: (total - points_used) * multiplier
            # Basitlik için Toplam Tutar üzerinden verelim.
            points = calculate_loyalty_points(new_sale.total_amount, customer.total_shopping_count)
            
            # 3. Update Balance (Add earned)
            customer.points_balance += points
            
            # 4. Link to Sale
            new_sale.customer_id = customer.id
            new_sale.loyalty_points_earned = points
            new_sale.loyalty_points_used = points_used
            points_earned = points
            
            db.add(customer)
            db.add(new_sale) # Update sale with customer_id

        await db.commit()
        await db.refresh(new_sale)

        # PDF & Mail (Background)
        if email and background_tasks:
             sale_dict = {
                 "receipt_no": new_sale.receipt_no,
                 "created_at": str(new_sale.created_at),
                 "pos_device_id": new_sale.pos_device_id,
                 "items": [{"product_sku": i.product_sku, "unit_price": i.unit_price, "quantity": i.quantity} for i in sale_data.items],
                 "total_amount": new_sale.total_amount,
                 "loyalty_points": points_earned # Add to context
             }
             filename = f"receipt_{new_sale.receipt_no}.pdf"
             background_tasks.add_task(process_receipt_delivery, email, sale_dict, filename)

        return {"message": "Sale processed", "receipt_no": new_sale.receipt_no, "id": new_sale.id, "points_earned": points_earned}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/returns")
async def create_pos_return(
    receipt_no: str,
    db: AsyncSession = Depends(get_db)
):
    """
    İade İşlemi.
    1. Satışı bul.
    2. Status -> RETURNED
    3. Stok Artır (ID: 9999)
    4. Sadakat Puanlarını İade Et (Kazanılanı geri al, harcananı iade et).
    """
    from models import Inventory, Product 
    
    # 1. Find Sale
    query = select(PosSale).where(PosSale.receipt_no == receipt_no)
    result = await db.execute(query)
    sale = result.scalar_one_or_none()
    
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
        
    if sale.status == "RETURNED":
         raise HTTPException(status_code=400, detail="Sale already returned")

    try:
        # Load items to process inventory
        # We need to fetch items. 
        # (Assuming items relationship is lazy, need explicit load or new query)
        # For simple query above, items might not be loaded.
        # Let's simple query items
        items_query = select(PosSaleItem).where(PosSaleItem.pos_sale_id == sale.id)
        items_res = await db.execute(items_query)
        items = items_res.scalars().all()
        
        # 2. Update Status
        sale.status = "RETURNED"
        
        # 3. Increment Stock (Store 9999)
        field_store_id = 9999
        
        for item in items:
            # Find Product
            prod_res = await db.execute(select(Product).where(Product.sku == item.product_sku))
            product = prod_res.scalar_one_or_none()
            
            if product:
                inv_res = await db.execute(select(Inventory).where(
                    Inventory.store_id == field_store_id,
                    Inventory.product_id == product.id
                ))
                inventory = inv_res.scalar_one_or_none()
                
                if inventory:
                    inventory.quantity += item.quantity
        
        # 4. Loyalty Reversal (Phase 8 Fix)
        if sale.customer_id:
            from models import Customer
            cust_res = await db.execute(select(Customer).where(Customer.id == sale.customer_id))
            customer = cust_res.scalar_one_or_none()
            
            if customer:
                # Refund used points
                if sale.loyalty_points_used > 0:
                    customer.points_balance += sale.loyalty_points_used
                
                # Deduct earned points
                if sale.loyalty_points_earned > 0:
                    customer.points_balance -= sale.loyalty_points_earned
                
                # Decrement shopping count
                if customer.total_shopping_count > 0:
                    customer.total_shopping_count -= 1
                
                db.add(customer)
        
        await db.commit()
        return {"message": "Return processed successfully", "receipt_no": receipt_no}
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

