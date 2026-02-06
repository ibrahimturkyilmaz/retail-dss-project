from models import Store, Inventory
from typing import Dict, List
from sqlalchemy.orm import Session

def analyze_store_risk(store: Store, db: Session = None) -> str:
    """
    Bir mağazanın stok risk durumunu belirler.
    Ürün bazlı envanter kontrolü yapar.
    """
    if not store.inventory:
        return "UNKNOWN"

    high_risk_count = 0
    overstock_count = 0
    total_items = 0

    for item in store.inventory:
        total_items += 1
        if item.quantity < item.safety_stock:
            high_risk_count += 1
        elif item.quantity > item.safety_stock * 3:
            overstock_count += 1
    
    if total_items == 0:
        return "LOW_RISK"

    # Eğer kritik ürünlerin %20'sinden fazlası riskliyse -> HIGH_RISK
    if (high_risk_count / total_items) > 0.2:
        return "HIGH_RISK"
    
    # Eğer ürünlerin %40'ı fazlaysa -> OVERSTOCK
    if (overstock_count / total_items) > 0.4:
        return "OVERSTOCK"
        
    return "LOW_RISK"

def get_risk_report(stores: List[Store]) -> List[Dict]:
    """
    Tüm mağazalar için risk raporu oluşturur.
    """
    report = []
    for store in stores:
        status = analyze_store_risk(store)
        
        # Stok toplamını hesapla
        total_stock = sum(item.quantity for item in store.inventory)
        total_safety = sum(item.safety_stock for item in store.inventory)

        # Frontend için renk kodları
        colors = {
            "HIGH_RISK": "red",
            "MEDIUM_RISK": "orange",
            "OVERSTOCK": "yellow",
            "LOW_RISK": "green",
            "UNKNOWN": "gray"
        }
        
        report.append({
            "store_id": store.id,
            "name": store.name,
            "type": store.store_type.value,
            "stock": total_stock,
            "safety_stock": total_safety,
            "status": status,
            "color": colors.get(status, "gray")
        })
    return report
