from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Store, Inventory, Sale, Product, StoreType
from seed import seed_data
from database import engine, Base
import random
from datetime import date

def simulate_sales_boom(db: Session):
    """
    Senaryo: Talep Patlaması 📈
    Rastgele mağazalarda stokları hızla tüketir ve satış kaydı oluşturur.
    Etki: Stoklar kritik seviyeye iner, ciro artar.
    """
    stores = db.query(Store).filter(Store.store_type == StoreType.STORE).all()
    impacted_count = 0
    total_sales_generated = 0
    
    for store in stores:
        # Mağazaların %70'i bu patlamadan etkilenir
        if random.random() > 0.3:
            impacted_count += 1
            for item in store.inventory:
                # Stok varsa %50-%90 arası satılır
                if item.quantity > 0:
                    sold_qty = int(item.quantity * random.uniform(0.5, 0.9))
                    if sold_qty > 0:
                        item.quantity -= sold_qty
                        
                        # Satış kaydı at (Ciro artsın)
                        sale = Sale(
                            store_id=store.id,
                            product_id=item.product_id,
                            customer_id=1, # Dummy customer
                            date=date.today(),
                            quantity=sold_qty,
                            total_price=sold_qty * item.product.price
                        )
                        db.add(sale)
                        total_sales_generated += sold_qty

    db.commit()
    return f"Talep Patlaması Simüle Edildi: {impacted_count} mağazada toplam {total_sales_generated} ürün satıldı. Stoklar eridi!"

def simulate_recession(db: Session):
    """
    Senaryo: Ekonomik Durgunluk 📉
    Mağazalara 'satılmayan' stok ekler.
    Etki: Stoklar şişer (Overstock).
    """
    stores = db.query(Store).filter(Store.store_type == StoreType.STORE).all()
    
    for store in stores:
        for item in store.inventory:
            # Her ürüne rastgele stok ekle (İade gelmiş veya depodan yığılmış gibi)
            unsold_qty = int(item.safety_stock * random.uniform(1.0, 3.0))
            item.quantity += unsold_qty
            
    db.commit()
    return f"Durgunluk Simüle Edildi: Tüm mağazalarda stoklar şişirildi (Overstock durumu yaratıldı)."

def simulate_supply_shock(db: Session):
    """
    Senaryo: Tedarik Krizi 🚚
    Tüm stokları (Hub ve Center dahil) %50 siler.
    Etki: Küresel yokluk.
    """
    inventories = db.query(Inventory).all()
    total_lost = 0
    
    for item in inventories:
        if item.quantity > 0:
            lost_qty = int(item.quantity * 0.5)
            item.quantity -= lost_qty
            total_lost += lost_qty
            
    db.commit()
    return f"Tedarik Krizi Simüle Edildi: Lojistik hatlarında {total_lost} ürün kaybedildi."

def reset_database(db: Session):
    """
    Veritabanını sıfırlar ve temiz verilerle (Seed) tekrar doldurur.
    """
    # 1. Tabloları temizle (Drop & Create yerine Delete All daha hızlı olabilir ama seed yapısı create bekliyor mu bakalım)
    # Seed.py içindeki logic tabloları drop edip create ediyor genelde.
    # Biz burada transaction güvenliği için Base.metadata kullanabiliriz.
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # 2. Seed işlemini çalıştır
    seed_data()
    
    return "Sistem Fabrika Ayarlarına Döndürüldü (Reset)."
