# ☁️ Bulut Servisleri Değerlendirme Raporu

**Proje:** Retail Decision Support System (DSS)  
**Tarih:** 15 Şubat 2026  
**Mimari:** Supabase (DB) + Render (Backend) + Vercel (Frontend)

---

## 1. Servis Avantajları Karşılaştırması

| Özellik | Supabase (DB) | Vercel (Frontend) | Render (Backend) |
|---|---|---|---|
| **Ana İşlev** | PostgreSQL + Auth + Realtime | Static site / SPA hosting | Python/Node backend hosting |
| **Ücretsiz Tier** | ✅ Cömert | ✅ Cömert | ✅ Var (kısıtlı) |
| **Setup Süresi** | ~5 dk | ~3 dk (GitHub bağla) | ~5 dk |
| **Auto Deploy** | — | ✅ Git push → otomatik | ✅ Git push → otomatik |
| **SSL/HTTPS** | ✅ Otomatik | ✅ Otomatik | ✅ Otomatik |
| **Custom Domain** | — | ✅ Ücretsiz | ✅ Ücretsiz |
| **CDN** | — | ✅ Global Edge Network | ❌ Tek bölge |
| **Dashboard** | ✅ SQL Editor, Table Viewer | ✅ Analytics, Logs | ✅ Logs, Metrics |
| **Ölçeklenebilirlik** | ✅ Otomatik | ✅ Otomatik | ⚠️ Manuel (free tier) |
| **Akademik Değer** | "Cloud-native, managed PostgreSQL" | "Edge-optimized CDN" | "Containerized microservice" |

---

## 2. Free Tier Limitleri vs Projemiz

### 2.1 Supabase Free Tier

| Limit | Supabase Veriyor | Projemiz Kullanıyor | Yeterli mi? |
|---|---|---|---|
| Veritabanı boyutu | **500 MB** | ~12 MB (retail.db) | ✅ **%2.4 kullanılıyor** |
| Satır sayısı | Sınırsız | ~350K satış + 7 mağaza + 15 ürün | ✅ Bol bol yeterli |
| API istekleri | Sınırsız | Dashboard açılışında ~10 istek | ✅ Sorun yok |
| Storage | 1 GB | Kullanmıyoruz (şimdilik) | ✅ |
| Edge Functions | 500K çağrı/ay | 0 (şimdilik) | ✅ |
| Auth | 50K kullanıcı | 1 (admin) | ✅ |
| Realtime | 200 eş zamanlı | 0 (şimdilik) | ✅ |
| **Uyku modu** | ❌ **7 gün inaktivitede uyur** | ⚠️ Düzenli kullanılmalı | ⚠️ Dikkat |

### 2.2 Vercel Free Tier (Hobby)

| Limit | Vercel Veriyor | Projemiz Kullanıyor | Yeterli mi? |
|---|---|---|---|
| Bandwidth | **100 GB/ay** | ~50 KB/sayfa yükleme | ✅ Çok yeterli |
| Build süresi | 6000 dk/ay | ~30 sn/build | ✅ |
| Serverless Functions | 100 GB-saat | 0 (backend Render'da) | ✅ |
| Deploy sayısı | Sınırsız | İhtiyaca göre | ✅ |
| Preview deploys | ✅ Her PR için | Git PR'ları test edebilirsin | ✅ |
| **Takım üyesi** | **1 kişi** | Tek geliştirici | ✅ |

### 2.3 Render Free Tier

| Limit | Render Veriyor | Projemiz Kullanıyor | Yeterli mi? |
|---|---|---|---|
| RAM | **512 MB** | FastAPI + pandas ~200 MB | ✅ Yeterli |
| CPU | Paylaşımlı | Tahmin işlemi CPU yoğun | ⚠️ Yavaş olabilir |
| Bandwidth | **100 GB/ay** | API JSON yanıtları ~1 KB | ✅ |
| Build süresi | 400 saat/ay | ~3 dk/build | ✅ |
| **Uyku modu** | ❌ **15 dk inaktivitede uyur** | ⚠️ İlk istek 30-50 sn sürer | ⚠️ Dikkat |
| Disk | ❌ Yok (ephemeral) | SQLite kullanılamaz → Supabase çözüyor | ✅ |

> **ÖNEMLİ:** Render free tier'ın en büyük kısıtı: 15 dakika kimse kullanmazsa sunucu uyur. İlk gelen istek "cold start" yaşar (~30-50 sn). **Çözüm:** UptimeRobot (ücretsiz) ile her 14 dk'da bir ping atarak sunucuyu uyanık tutmak.

### 2.4 Maliyet Özeti

| Servis | Plan | Aylık Maliyet | Not |
|---|---|---|---|
| Supabase | Free | **$0** | 500 MB DB, yeterli |
| Vercel | Hobby | **$0** | 100 GB bandwidth |
| Render | Free | **$0** | 512 MB RAM, cold start var |
| UptimeRobot | Free | **$0** | 50 monitör |
| **Toplam** | — | **$0/ay** | 💰 Tamamen ücretsiz |

---

## 3. Deployment Sonrası Ne Değişir?

| Konu | Lokal (Şu An) | Cloud (Sonra) |
|---|---|---|
| **Erişim** | Sadece `localhost` | `retail-dss.vercel.app` gibi public URL |
| **Veri güvenliği** | Disk bozulursa kayıp | Supabase otomatik yedekleme |
| **Demo/Sunum** | Laptop açıp çalıştırmak lazım | Link paylaş, bitti |
| **CV/Portföy** | "Kodu var ama gösteremem" | "Buyrun canlı link" → **büyük fark** |
| **Hoca/Jüri** | Ekran paylaşımı gerekir | Kendi telefonlarından bakabilirler |
| **CI/CD** | Git push → elle deploy | Git push → **otomatik deploy** |
| **Monitoring** | Yok | Vercel Analytics + Render logs |
| **Çoklu cihaz** | Sadece geliştirme makinesi | Tüm cihazlar (responsive) |

---

## 4. Proje Özelinde İyileştirme Fırsatları

### 4.1 🏗️ Backend Mimarisi

#### Mevcut Durum
`main.py` → 1863 satır, 40+ endpoint, tüm iş mantığı tek dosyada.

#### İyileştirmeler

| # | İyileştirme | Detay | Etki |
|---|---|---|---|
| 1 | **Router Ayrıştırma** | `main.py`'deki endpointler `routers/` klasörüne ayrılmalı: `stores.py`, `sales.py`, `transfers.py`, `ai.py`, `calendar.py`, `playground.py` | Okunabilirlik ↑ %80 |
| 2 | **Schema Ayrıştırma** | Pydantic modelleri `schemas/` klasörüne taşınmalı (şu an main.py içinde inline tanımlı) | Bakım kolaylığı |
| 3 | **Service Layer** | Endpoint'ler direkt DB sorgusu yapıyor → Arada `services/` katmanı olmalı | Test edilebilirlik ↑ |
| 4 | **customer_id Bug Fix** | `Sale` modelinde `customer_id` FK eksik. `seed.py` bu kolonu yazıyor ama `models.py`'de tanımlı değil. SQLite bunu sessizce yuttu ama PostgreSQL hata verecek | **Kritik** |
| 5 | **N+1 Query Sorunu** | `export_sales_report` endpoint'i döngü içinde her satır için ayrı `Store` ve `Product` sorgusu yapıyor (satır 1006-1007). `joinedload` kullanılmalı | Performans ↑ %90 |
| 6 | **Duplicate Endpoint** | `/api/analysis/model-metrics` (satır 801) ve `/analysis/model-metrics` (satır 1818) → Aynı işlev iki kez tanımlı | Temizlik |
| 7 | **Dead Code** | `main.py` satır 1644-1646: `db.delete(note)` bloğu return sonrası → **Ulaşılamaz kod** (Erişilemeyen kod) | Bug |
| 8 | **Rate Limiter Memory Leak** | `_ai_rate_limits` dict'i sunucu yeniden başlamadıkça temizlenmiyor. Çok kullanıcıda memory şişer | Stabilite |

#### Öneri: Yeni Klasör Yapısı
```
backend/
├── main.py              (Sadece app = FastAPI() + router mount)
├── core/
│   ├── config.py
│   └── logger.py
├── models/
│   ├── __init__.py
│   ├── store.py
│   ├── product.py
│   ├── sale.py
│   └── user.py
├── schemas/
│   ├── store.py
│   ├── transfer.py
│   └── user.py
├── routers/
│   ├── stores.py
│   ├── sales.py
│   ├── transfers.py
│   ├── simulations.py
│   ├── ai.py
│   ├── calendar.py
│   └── playground.py
├── services/
│   ├── risk_engine.py
│   ├── transfer_engine.py
│   └── forecast_service.py
└── requirements.txt
```

---

### 4.2 🗄️ Veritabanı İyileştirmeleri

| # | İyileştirme | Detay | Etki |
|---|---|---|---|
| 1 | **Index Eksikleri** | `sales` tablosunda `(store_id, product_id, date)` composite index yok. Forecast ve analiz sorguları yavaş | Sorgu hızı ↑ 5-10x |
| 2 | **Enum Typing** | `StoreType` enum'u PostgreSQL'de `VARCHAR` olarak saklanıyor. Native `ENUM` type kullanılmalı | Type safety |
| 3 | **Soft Delete** | Transferler ve notlar kalıcı olarak siliniyor → `is_deleted` flag + `deleted_at` timestamp eklenebilir | Veri güvenliği |
| 4 | **Audit Trail** | Stok değişikliklerinin logu tutulmuyor. Kim, ne zaman, ne değiştirdi? `stock_audit_log` tablosu eklenebilir | Akademik değer ↑ |
| 5 | **Supabase RLS** | Row Level Security ile her kullanıcı sadece kendi mağazasının verisini görebilir → Multi-tenant mimari | Güvenlik + akademik |
| 6 | **Database Migrations** | Şu an `Base.metadata.create_all()` ile tablo oluşturuluyor. `Alembic` ile migration yönetimi yapılmalı | Production-ready |

#### Supabase'e Özgü Fırsatlar

```sql
-- Örnek: Stok kritik seviyeye düşünce otomatik trigger
CREATE OR REPLACE FUNCTION notify_low_stock()
RETURNS trigger AS $$
BEGIN
    IF NEW.quantity < NEW.safety_stock THEN
        PERFORM pg_notify('low_stock', json_build_object(
            'store_id', NEW.store_id,
            'product_id', NEW.product_id,
            'quantity', NEW.quantity
        )::text);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER low_stock_trigger
    AFTER UPDATE ON inventory
    FOR EACH ROW EXECUTE FUNCTION notify_low_stock();
```

---

### 4.3 🎨 Frontend İyileştirmeleri

#### Mevcut Durum
40 JSX component, React Query ile veri çekme, Leaflet harita, Recharts grafikler.

| # | İyileştirme | Detay | Etki |
|---|---|---|---|
| 1 | **Error Boundary** | Herhangi bir component hata verirse tüm sayfa çöküyor → React Error Boundary eklenebilir | UX ↑ |
| 2 | **Loading Skeleton** | Veri yüklenirken boş ekran → Skeleton placeholder animasyonları | UX ↑ |
| 3 | **Optimistic Updates** | Transfer onaylandığında sayfa yenileniyor → React Query `optimisticUpdate` ile anında UI güncelleme | UX ↑ |
| 4 | **Code Splitting** | Tüm sayfalar tek bundle'da → `React.lazy()` ile sayfa bazlı lazy loading | İlk yükleme ↓ %40 |
| 5 | **PWA Desteği** | `manifest.json` + service worker → Telefona "yükle" butonu, offline temel erişim | Erişilebilirlik ↑ |
| 6 | **i18n (Çoklu Dil)** | Şu an tüm metinler Türkçe hardcoded → `react-i18next` ile EN/TR desteği | Akademik + global |
| 7 | **Dark/Light Persistence** | Tema tercihinin localStorage'da saklanması (şu an `ThemeContext` var ama kalıcılık kontrol edilmeli) | UX ↑ |
| 8 | **Responsive Tablo** | `StockTable.jsx` geniş ekrandan telefona geçince taşıyor olabilir → horizontal scroll veya card view | Mobile UX |

---

### 4.4 🤖 AI & ML İyileştirmeleri

| # | İyileştirme | Detay | Etki |
|---|---|---|---|
| 1 | **Prophet → Cloud** | Şu an Colab'da eğitim + CSV import. Supabase Edge Function'a cron ile otomatik eğitim eklenebilir | Otomasyon |
| 2 | **Forecast Confidence** | Mevcut lineer regresyon güven skoru yok → Prophet'in `yhat_lower/yhat_upper` band'ları kullanılabilir | Akademik ↑ |
| 3 | **Feature Engineering** | `Sale` modelinde `weather`, `holiday`, `promotion` kolonları var ama kullanılmıyor → Tahmin modeline dahil edilmeli | Model kalitesi ↑ |
| 4 | **A/B Test Transfer** | Robin Hood v2.2 ile v3 algoritmasını karşılaştırmak için A/B test altyapısı | Akademik ↑ |
| 5 | **Anomaly Detection** | Beklenmedik satış spike'ları veya düşüşleri tespit → Z-score veya IQR bazlı alarm | Proaktif yönetim |
| 6 | **Gemini Streaming** | Şu an tam yanıt beklenip dönüyor → SSE (Server-Sent Events) ile streaming yanıt | UX ↑ |

---

### 4.5 🔐 Güvenlik İyileştirmeleri

| # | İyileştirme | Detay | Öncelik |
|---|---|---|---|
| 1 | **Gerçek Auth** | Şu an `admin/123` hardcoded. Supabase Auth ile JWT tabanlı gerçek kimlik doğrulama | 🔴 Kritik |
| 2 | **Password Hashing** | `models.py` satır 143: şifre plain text → `bcrypt` ile hash'lenip saklanmalı | 🔴 Kritik |
| 3 | **CORS Güvenliği** | `origins = ["*"]` → Sadece Vercel domain + localhost izin vermeli | 🟡 Yüksek |
| 4 | **API Key Rotation** | `.env`'deki Gemini ve Weather API key'leri expose olmuş (git geçmişinde). Yenilenmeli | 🟡 Yüksek |
| 5 | **SQL Injection** | SQL Playground endpoint'i sadece keyword kara listesi ile korunuyor → Parameterized query + whitelist | 🟡 Orta |
| 6 | **Rate Limit Bypass** | SlowAPI IP bazlı → Proxy/VPN ile bypass edilebilir. Token bazlı rate limit daha güvenli | 🟢 Düşük |

---

### 4.6 📊 Monitoring & DevOps

| # | İyileştirme | Detay | Servis |
|---|---|---|---|
| 1 | **Uptime Monitoring** | UptimeRobot ile backend ve frontend uptime izleme + email alert | UptimeRobot (ücretsiz) |
| 2 | **Error Tracking** | Frontend hataları loglanmıyor → Sentry (ücretsiz tier: 5K event/ay) | Sentry |
| 3 | **APM (Performance)** | API endpoint'lerin yanıt süreleri izlenmiyor → Render metrics + custom logging | Render |
| 4 | **CI/CD Pipeline** | GitHub Actions ile: lint → test → build → deploy otomatik pipeline | GitHub Actions (ücretsiz) |
| 5 | **Staging Ortamı** | Vercel preview deployments → Her PR için otomatik staging URL | Vercel |
| 6 | **Health Check** | `/health` endpoint'i yok → DB bağlantısı, disk, memory kontrolü dönen health endpoint | Backend |

---

### 4.7 📈 İş Zekası (BI) İyileştirmeleri

| # | İyileştirme | Detay | Etki |
|---|---|---|---|
| 1 | **Karşılaştırmalı Analiz** | Mağazalar arası performans karşılaştırma dashboard'u (benchmark) | Karar destek ↑ |
| 2 | **Kohort Analizi** | Müşterileri ilk alışveriş tarihine göre grupla, retention oranlarını izle | Akademik ↑ |
| 3 | **Basket Analysis** | Hangi ürünler birlikte satılıyor? → Apriori algoritması ile cross-sell önerileri | Gelir ↑ |
| 4 | **KPI Alert Sistemi** | Belirlenen eşik değerlerin altına düşünce otomatik email/push bildirim | Proaktiflik ↑ |
| 5 | **Custom Dashboard** | Kullanıcının kendi widget'larını sürükle-bırak ile yerleştirebilmesi (mevcut `DraggableDashboard` genişletilebilir) | UX ↑ |
| 6 | **Rapor Zamanlama** | Haftalık/aylık otomatik rapor oluşturup email ile gönderme (Supabase cron + Edge Functions) | Otomasyon |

---

## 5. Ekstra Yapılabilecekler (Deployment Sonrası)

### 5.1 Hemen Yapılabilecekler

| Özellik | Servis | Açıklama |
|---|---|---|
| **🔐 Supabase Auth** | Supabase | Email/şifre login, JWT, oturum yönetimi → Hardcoded auth yerine |
| **📊 Vercel Analytics** | Vercel | Sayfa ziyaret istatistikleri, kullanıcı davranışları |
| **🔔 UptimeRobot** | Harici | Backend uyumasın + uptime monitoring + email alert |
| **🌐 Custom Domain** | Vercel + Render | `retaildss.com` gibi kendi domain'i bağlama |
| **🏥 Health Check** | Backend | `/health` endpoint: DB bağlantı durumu, uptime, versiyon bilgisi |

### 5.2 Kısa Vadede (1-2 Hafta)

| Özellik | Servis | Açıklama |
|---|---|---|
| **⚡ Supabase Realtime** | Supabase | Stok değiştiğinde dashboard anlık güncellenir (WebSocket). Şu an yenileme gerekiyor |
| **📱 PWA** | Vercel | Telefona "yükle" butonu, offline temel erişim, push notification altyapısı |
| **⏰ Scheduled Forecasting** | Render Cron | Her gece otomatik tahmin güncelleme (şu an elle tetikleniyor) |
| **📧 Stok Alert Sistemi** | Supabase + Edge | Stok kritik seviyeye düşünce otomatik email gönderimi |
| **🗃️ Rapor Storage** | Supabase Storage | Oluşturulan Excel/CSV raporları bulutta saklama ve paylaşma |

### 5.3 Orta Vadede (1 Ay)

| Özellik | Servis | Açıklama |
|---|---|---|
| **🔄 CI/CD Pipeline** | GitHub Actions | lint → test → build → deploy otomatik pipeline |
| **🌍 i18n Desteği** | Frontend | İngilizce/Türkçe dil seçeneği → Uluslararası erişim |
| **📊 Sentry Entegrasyonu** | Sentry | Frontend + backend hata izleme ve raporlama |
| **🧪 E2E Test** | Playwright | Kritik akışların (transfer, simülasyon) otomatik test senaryoları |
| **🗄️ Alembic Migration** | Backend | Veritabanı şema değişikliklerinin versiyonlanması |

### 5.4 İleri Seviye (Akademik Değer Katan)

| Özellik | Değer |
|---|---|
| **Row Level Security (RLS)** | Her kullanıcı sadece kendi mağazasının verisini görür. Tez'de "multi-tenant security architecture" |
| **Database Webhooks** | Veritabanı değişikliğinde otomatik aksiyon tetikleme (örn: stok düşünce transfer önerisi) |
| **Edge Functions AI** | Gemini çağrısını Supabase Edge Function'a taşıyarak backend bağımsızlığı |
| **A/B Testing** | Vercel built-in A/B test desteği ile farklı dashboard tasarımlarını karşılaştırma |
| **Branching Preview** | Her Git branch'i için ayrı preview URL — "şu özelliği test edin" diye link paylaşmak |
| **Anomaly Detection** | Z-score bazlı otomatik satış anomalisi tespiti ve alarm sistemi |
| **Basket Analysis** | Apriori algoritması ile ürün birliktelik analizi ve cross-sell önerileri |

---

## 6. Öncelik Matrisi

```
                    ETKİ YÜKSEK
                        |
    ┌───────────────────┼───────────────────┐
    │  Supabase Auth    │  Router Ayrıştırma│
    │  CORS Fix         │  N+1 Query Fix    │
    │  customer_id Fix  │  Health Check     │
    │                   │  Alembic          │
    │   HEMEN YAP       │   PLANLA          │
    ├───────────────────┼───────────────────┤
    │  UptimeRobot      │  PWA              │
    │  Error Boundary   │  i18n             │
    │  Loading Skeleton │  Basket Analysis  │
    │                   │  E2E Test         │
    │   KOLAY KAZANIM   │   İLERDE          │
    └───────────────────┼───────────────────┘
                        |
                    ETKİ DÜŞÜK
     EFOR DÜŞÜK ◄──────┼──────► EFOR YÜKSEK
```
