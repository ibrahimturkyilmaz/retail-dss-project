# Retail DSS - Perakende Karar Destek Sistemi 🚀

Modern perakende zincirleri için geliştirilmiş, yapay zeka destekli stok yönetimi, dağıtım optimizasyonu ve senaryo simülasyonu sistemi.

![Project Preview](frontend-icin-ornek-gorsel/dashboard-preview.png)

## 🌟 Özellikler

*   **📊 Gerçek Zamanlı Dashboard:** Ciro, stok ve satış trendlerinin anlık takibi.
*   **🧠 Akıllı Transfer Önerileri (XAI):** Merkez -> Hub -> Mağaza hiyerarşisine uygun, nedenleriyle açıklanmış stok transfer önerileri.
*   **⚡ Senaryo Simülasyonu:** "Talep Patlaması", "Ekonomik Durgunluk" gibi kriz senaryolarının sistem üzerindeki etkilerini test etme.
*   **🗺️ İnteraktif Harita:** İstanbul genelindeki mağaza ağının ve lojistik akışının görselleştirilmesi.
*   **🔮 Talep Tahmini:** Basit doğrusal regresyon ile gelecek satış tahminleri.

## 🛠️ Teknolojiler

### Backend
*   **Python (FastAPI):** Yüksek performanslı API.
*   **PostgreSQL:** İlişkisel veritabanı.
*   **SQLAlchemy:** ORM katmanı.
*   **Pandas & Scikit-learn:** Veri analizi ve tahminleme.

### Frontend
*   **React (Vite):** Hızlı ve modern UI.
*   **Tailwind CSS v4:** Premium ve responsive tasarım.
*   **TanStack Query:** Veri yönetimi ve önbellekleme.
*   **Leaflet:** Harita görselleştirme.

## 🚀 Kurulum

### 1. Ön Gereksinimler
*   Python 3.9+
*   Node.js 18+
*   PostgreSQL

### 2. Backend Kurulumu
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Veritabanını oluşturun ve örnek verilerle doldurun:
```bash
python seed.py
```

Sunucuyu başlatın:
```bash
uvicorn main:app --reload
```

### 3. Frontend Kurulumu
```bash
cd frontend
npm install
npm run dev
```

## ⚙️ Yapılandırma
Proje kök dizininde `.env` dosyası oluşturarak veritabanı ayarlarını özelleştirebilirsiniz (Varsayılan: localhost).

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345
DB_NAME=retail_dss
```

## 🧪 Lisans
Bu proje eğitim amaçlı geliştirilmiştir (END401 Bitirme Projesi).
