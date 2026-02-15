import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Forecast, Product, Store
import datetime

def import_forecasts(csv_path="forecast_results.csv", store_id=1, product_id=1):
    print(f"📥 Importing forecasts from {csv_path} for Store {store_id}, Product {product_id}...")
    
    db = SessionLocal()
    try:
        # 1. CSV Oku
        df = pd.read_csv(csv_path)
        print(f"✅ CSV Loaded. Rows: {len(df)}")
        
        # 2. Eski tahminleri temizle (Bu ürün ve mağaza için)
        db.query(Forecast).filter(
            Forecast.store_id == store_id,
            Forecast.product_id == product_id
        ).delete()
        db.commit()
        print("🧹 Old forecasts cleared.")
        
        # 3. Yeni verileri ekle
        forecasts_buffer = []
        
        for _, row in df.iterrows():
            # Prophet 'ds' string dönebilir, date objesine çevir
            date_val = pd.to_datetime(row['ds']).date()
            
            # Sadece bugünden sonrasını al (Gelecek tahmini)
            # Ancak Prophet geçmişi de fit ettiği için hepsini kaydedebiliriz,
            # Grafik çizimi için geçmiş + gelecek verisi güzel olur.
            
            yhat = row['yhat']
            yhat_lower = row['yhat_lower']
            yhat_upper = row['yhat_upper']
            
            # Güven Skoru Hesabı (Kalibre Edilmiş v3)
            # Perakende tahminlerinde band/tahmin oranı 0.5-1.5 normaldir.
            # Bu formül: ratio=0.5 → %90, ratio=1.0 → %80, ratio=2.0 → %55
            band_width = abs(yhat_upper - yhat_lower)
            if abs(yhat) > 1:
                ratio = band_width / abs(yhat)
                # Exponential decay: daha gerçekçi kalibrasyon
                import math
                confidence_score = max(0, min(100, 100 * math.exp(-0.18 * ratio)))
            else:
                confidence_score = 50
            
            # Eksi tahminleri sıfırla
            predicted_qty = max(0, yhat)
            
            forecasts_buffer.append({
                "store_id": store_id,
                "product_id": product_id,
                "date": date_val,
                "predicted_quantity": predicted_qty,
                "confidence_lower": max(0, yhat_lower),
                "confidence_upper": max(0, yhat_upper),
                "confidence_score": round(confidence_score, 2),
                "model_name": "Prophet (Colab)"
            })
            
        # Bulk Insert
        db.bulk_insert_mappings(Forecast, forecasts_buffer)
        db.commit()
        print(f"✅ Successfully imported {len(forecasts_buffer)} forecast records.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_forecasts()
