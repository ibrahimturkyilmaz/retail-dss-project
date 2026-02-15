import pandas as pd
from sqlalchemy.orm import Session
from models import Sale
import io

def export_training_data(db: Session, store_id: int, product_id: int):
    """
    Belirli bir mağaza ve ürün için satış verilerini Prophet formatında (ds, y)
    CSV olarak hazırlar.
    """
    # 1. Veriyi Sorgula
    query = db.query(Sale.date, Sale.quantity).filter(
        Sale.store_id == store_id,
        Sale.product_id == product_id
    )
    
    # 2. Pandas DataFrame'e Çevir
    df = pd.read_sql(query.statement, db.bind)
    
    if df.empty:
        return None
        
    # 3. İsimlendirme (Prophet Standardı)
    df.columns = ['ds', 'y']
    
    # 4. Toplaştırma (Günlük Toplam Satış)
    # Aynı gün içinde birden fazla satış kaydı olabilir, bunları toplamalıyız.
    df = df.groupby('ds')['y'].sum().reset_index()
    
    # 5. Eksik Tarihleri Doldurma (Resampling)
    # Satış olmayan günleri 0 olarak ekle
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.set_index('ds').resample('D').sum().fillna(0).reset_index()
    
    # 6. CSV'ye Çevir (String olarak)
    output = io.StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()
