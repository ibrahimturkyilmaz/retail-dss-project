# 📂 RetailDSS - Proje Yapısı ve Bileşenler Tablosu

Aşağıdaki tablo, projenin ana işlem kollarını (branches), ilgili klasörleri ve teknolojik altyapılarını özetler.

| **Bileşen (Project Arm)** | **Klasör (Path)** | **Teknoloji Stack'i** | **Açıklama (Description)** | **Durum** |
| :--- | :--- | :--- | :--- | :--- |
| **Backend API** | `/backend` | Python, FastAPI, SQLAlchemy | Ana sunucu mantığı, veritabanı iletişimi, AI motoru (Gemini), e-posta servisi ve iş kuralları burada çalışır. | ✅ Aktif |
| **Frontend (Dashboard)** | `/frontend` | React 19, Vite, TailwindCSS | Yönetim paneli, raporlama ekranları, simülasyon arayüzü ve admin işlemleri için web uygulaması. | ✅ Aktif |
| **Mobil Uygulama** | `/mobile` | React Native (Expo), Supabase | Müşteriler için alışveriş uygulaması ve saha çalışanları için operasyonel işlemler. | 🚧 Geliştiriliyor |
| **Veritabanı** | `retail.db` | SQLite (Dev) / PostgreSQL (Prod) | Mağaza, ürün, stok, satış ve müşteri verilerinin tutulduğu merkezi veritabanı. | ✅ Aktif |
| **AI Servisleri** | `/backend/core` & `/backend/services` | Google Gemini API, Scikit-Learn | Talep tahmini (Forecasting), Simülasyon motoru ve Text-to-SQL asistanı servisleri. | ✅ Aktif |
| **Dokümantasyon** | `/docs` & `*.md` | Markdown | Proje teknik raporları, ekran görüntüleri, kurulum kılavuzları ve API dokümantasyonu. | ✅ Güncel |
| **Testler** | `test_*.py` | Pytest, Requests | Backend endpoint'leri, e-posta gönderimi ve iş mantığı için doğrulama testleri. | 🟡 Kısmi |

---

## 📌 Modül Detayları

### 1. Backend (`/backend`)
- **Routers:** `users`, `products`, `stores`, `sales`, `simulation`, `pos`.
- **Core:** Konfigürasyon (`config.py`), Loglama, E-posta (`email.py`).
- **Models & Schemas:** Veritabanı tabloları ve Pydantic veri şemaları.

### 2. Frontend (`/frontend`)
- **Pages:** Dashboard, Simulation, Users, Inventory, POS.
- **Components:** Recharts Grafikleri, Leaflet Haritaları, Dinamik Tablolar.

### 3. Mobile (`/mobile`)
- **Screens:** Login, Home, Shop, Profile.
- **Context:** User, Cart, Location (Geofencing).
- **Services:** Supabase Auth, API Client.
