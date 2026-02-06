from models import Store, StoreType
from risk_engine import analyze_store_risk
from typing import List, Dict
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Haversine formülü ile iki nokta arası mesafe (km).
    """
    R = 6371 # Dünya yarıçapı (km)
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def generate_transfer_recommendations(stores: List[Store], max_truck_capacity: int = 50) -> List[Dict]:
    """
    Gelişmiş Transfer Algoritması (Hiyerarşik + XAI):
    Öncelik Sırası:
    1. HUB (Ara Depo)
    2. CENTER (Merkez Depo)
    3. STORE (Kardeş Mağaza - En Yakın)
    
    Her öneri için "Neden?" sorusunu cevaplayan XAI verisi üretir.
    """
    
    recommendations = []
    transfer_id_counter = 100
    
    # Envanteri analiz et
    # İhtiyacı olanlar (Receivers) ve Fazlası olanlar (Givers)
    receivers = []
    givers = {StoreType.HUB: [], StoreType.CENTER: [], StoreType.STORE: []}
    
    # 1. Havuzları Doldur
    for store in stores:
        for item in store.inventory:
            # Alıcı mı? (Aciliyet Skoru: Stok 0 ise 1.0, yarı ise 0.5)
            if item.quantity < item.safety_stock:
                shortage = item.safety_stock - item.quantity
                priority = 1 - (item.quantity / item.safety_stock) if item.safety_stock > 0 else 1.0
                receivers.append({
                    "store": store,
                    "product": item.product,
                    "shortage": shortage,
                    "priority": priority,
                    "current_stock": item.quantity,
                    "safety_stock": item.safety_stock
                })
            
            # Verici mi? (Güvenlik stoğunun 2 katından fazlası varsa vericidir)
            # HUB ve CENTER için kural: Güvenlik stoğunun üstündeki her şey verilebilir.
            elif item.quantity > item.safety_stock:
                excess = 0
                if store.store_type in [StoreType.HUB, StoreType.CENTER]:
                     excess = item.quantity - item.safety_stock # Depolar cömerttir
                elif item.quantity > (item.safety_stock * 2):
                     excess = item.quantity - (item.safety_stock * 2) # Mağazalar cimridir

                if excess > 0:
                    givers[store.store_type].append({
                        "store": store,
                        "product_id": item.product_id,
                        "excess": excess,
                        "current_stock": item.quantity
                    })

    # 2. Önceliğe Göre Sırala (En acil olanlar önce çözülür)
    receivers.sort(key=lambda x: x["priority"], reverse=True)
    
    # 3. Eşleştirme Algoritması
    for req in receivers:
        needed_product_id = req["product"].id
        amount_needed = req["shortage"]
        
        # SIRA 1: HUB Kontrolü
        # SIRA 2: CENTER Kontrolü
        # SIRA 3: STORE Kontrolü
        
        search_order = [StoreType.HUB, StoreType.CENTER, StoreType.STORE]
        best_source = None
        min_dist = float('inf')
        
        for source_type in search_order:
            potential_givers = [g for g in givers[source_type] if g["product_id"] == needed_product_id and g["excess"] > 0]
            
            if not potential_givers:
                continue # Bu türde kaynak yok, bir sonrakine bak
                
            # Bu türdeki en uygun (en yakın) kaynağı bul
            for giver in potential_givers:
                dist = calculate_distance(req["store"].lat, req["store"].lon, giver["store"].lat, giver["store"].lon)
                # Basit optimizasyon: İlk bulduğumuzu değil, en yakınını alalım
                if dist < min_dist:
                    min_dist = dist
                    best_source = giver
            
            if best_source:
                # Kaynak bulundu! Döngüyü kır (Hiyerarşi kuralı: Hub varsa Store'a bakma)
                break 
        
        if best_source:
            # Transfer miktarını belirle
            transfer_amount = min(amount_needed, best_source["excess"], max_truck_capacity)
            
            # Kaynağın stoğunu sanal olarak düşür (aynı döngüde başkasına vermesin)
            best_source["excess"] -= transfer_amount
            
            source_store = best_source["store"]
            target_store = req["store"]
            product_name = req["product"].name
            
            # --- XAI (Açıklanabilir Yapay Zeka) ---
            # Kararın nedenlerini doğal dilde açıkla
            explanations = []
            
            # Neden Hedef Seçildi?
            stock_ratio = int((req["current_stock"] / req["safety_stock"]) * 100) if req["safety_stock"] > 0 else 0
            explanations.append(f"Hedef mağaza {target_store.name}'da stok kritik seviyede (%{stock_ratio}).")
            
            # Neden Kaynak Seçildi?
            if source_store.store_type == StoreType.HUB:
                explanations.append(f"Öncelik Kuralı: En yakın HUB ({source_store.name}) tercih edildi.")
            elif source_store.store_type == StoreType.CENTER:
                 explanations.append(f"Öncelik Kuralı: Yerel stok yetersiz, Merkez Depo devreye girdi.")
            else:
                 explanations.append(f"Verimlilik: {source_store.name} mağazasında atıl stok ({best_source['current_stock']} adet) tespit edildi.")

            # Maliyet/Lojistik
            explanations.append(f"Lojistik: Mesafe {min_dist:.1f} km (Uygun).")
            
            rec = {
                "transfer_id": f"TRF-{transfer_id_counter}",
                "source": {
                    "id": source_store.id,
                    "name": source_store.name,
                    "type": source_store.store_type.value
                },
                "target": {
                    "id": target_store.id,
                    "name": target_store.name,
                    "type": target_store.store_type.value
                },
                "product": product_name, 
                "amount": transfer_amount,
                "xai_explanation": { # Frontend'de kart olarak gösterilecek
                    "summary": f"{source_store.name} ➔ {target_store.name}",
                    "reasons": explanations,
                    "score": round(req["priority"] * 100) # Aciliyet Skoru (0-100)
                },
                "algorithm": "Hierarchical-XAI v1.0"
            }
            recommendations.append(rec)
            transfer_id_counter += 1

    return recommendations
