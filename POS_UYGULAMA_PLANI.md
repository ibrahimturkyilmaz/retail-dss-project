# PWA POS Terminal Uygulama Planı (Detaylı & Türkçe)

## 🎯 Hedef
**"Depo -> Mağaza -> Kasa (POS)"** akışını tamamlayan, internet kesintisine dayanıklı ve modern donanım simülasyonlarına sahip profesyonel bir satış ekranı geliştirmek.

## 1. Veritabanı ve Backend Geliştirmesi
Güvenilir bir stok düşüşü ve satış kaydı için işlemler sunucu tarafında (Backend) yapılmalıdır.
*   **Endpoint:** `POST /api/sales` (Atomic Transaction)
*   **İş Mantığı:**
    1.  **Stok Kontrolü:** `Inventory` tablosundan mağaza ve ürün stokunu kontrol et.
    2.  **Yetersiz Stok Hatası:** Eğer `stok < satılan_adet` ise `400 Bad Request` dön.
    3.  **Stok Düşüşü:** `Inventory.quantity` değerini azalt.
    4.  **Satış Kaydı:** `Sales` tablosuna yeni kayıt ekle (Tarih, Miktar, Toplam Tutar).
    5.  **Commit:** Tüm işlemleri tek seferde onayla (Hata durumunda Rollback).

## 2. Dosya ve Klasör Yapısı
Projenin temiz ve sürdürülebilir olması için aşağıdaki yapı kullanılacaktır:
*   **`src/services/syncService.js`**: Offline satışların yönetimi ve senkronizasyon mantığı.
*   **`src/hooks/useBarcodeScanner.js`**: Akıllı barkod okuma (zamanlama bazlı) hook'u.
*   **`src/components/pos/`**:
    *   `BarcodeScanner.jsx`: Kamera tabanlı barkod okuyucu (Mobil için).
    *   `CheckoutModal.jsx`: Ödeme ve fiş seçenekleri.
    *   `ReceiptPreview.jsx`: Dijital fiş (QR/PDF) görünümü.
    *   `SyncIndicator.jsx`: Bağlantı ve senkronizasyon durumu.

## 3. Navigasyon ve "SAHA" Sekmesi
Mobil kullanıcılar için özel bir navigasyon deneyimi kurgulanacaktır:
*   **`constants/navigation.js`**:
    *   `SAHA` öğesi eklenecek: `{ name: 'SAHA', path: '/pos', icon: QrCodeIcon, mobileOnly: true }`.
*   **`components/Dock.jsx` (Desktop):** `mobileOnly` olan öğeleri filtreleyip göstermeyecek.
*   **`components/MobileNav.jsx` (Yeni):**
    *   Sadece `md` ekran altı görünür (`block md:hidden`).
    *   Ekranın altında sabit (Fixed Bottom) duran modern bir "Bottom Navigation" çubuğu.
    *   "SAHA" sekmesi burada en vurgulu (orta kısımda veya özel renkte) yer alacak.

## 3.1. Giriş ve Rol Bazlı Dinamik Arayüz (Zorunlu)
**Mantık:** Kullanıcı login ekranında OFİS veya SAHA modunu seçmek zorundadır. Bu seçim, arayüzü kökten değiştirir.

1.  **Login Ekranı:**
    *   İki Dev Buton: **🏢 OFİS GİRİŞİ** (Dashboard) ve **🛒 SAHA GİRİŞİ** (POS).
    *   **Yetki Kontrolü:** Sadece `role='saha'` veya `admin` olanlar SAHA butonunu kullanabilir.
    *   **Garanti:** Mobilde giren biri yanlışlıkla Dashboard'u açamaz.

### 3.1.1. Cihaz Tespiti ve Erişim Kontrolü (Device Validation)
Sistem, kullanıcının girdiği cihazı (`User-Agent` üzerinden) tespit edecek ve aşağıdaki kuralları **kati suretle** uygulayacaktır:

| Kullanıcı Rolü | Tespit Edilen Cihaz | Sonuç | Aksiyon / Uyarı Mesajı |
| :--- | :--- | :--- | :--- |
| **SAHA** | 📱 MOBILE / TABLET | ✅ **BAŞARILI** | POS Ekranına Yönlendir (`/pos`). |
| **SAHA** | 💻 DESKTOP | ❌ **REDDEDİLDİ** | *"Lütfen mobil cihazdan giriş yapın."* |
| **OFİS** | 💻 DESKTOP | ✅ **BAŞARILI** | Dashboard Ekranına Yönlendir (`/dashboard`). |
| **OFİS** | 📱 MOBILE / TABLET | ❌ **REDDEDİLDİ** | *"Dashboard mobil erişime kapalıdır. Masaüstünden girin."* |

## 3.2. Saha Modu: Barkod Simülasyonu ve Satış Akışı

Gerçek bir barkod sistemi yerine, sunum/demo için **"Kamera Simülasyonu"** kurgulanacaktır.

1.  **Barkod Okuma (Simülasyon):**
    *   Kamera açılır (`<BarcodeScanner />`).
    *   Herhangi bir QR/Barkod okutulduğunda (veya rastgele tetiklendiğinde), sistem simülasyon moduna geçer.
    *   **Rastgele Ürün Getirme:** Okunan barkod ne olursa olsun, veritabanından **rastgele bir ürün** seçilir ve ekrana getirilir.
    *   **Amaç:** Demoda barkodsuz ürünlerle bile hızlıca satış yapıldığını göstermek.

2.  **Müşteri ve Mail (Zorunlu):**
    *   Ürünler onaylandıktan sonra "Müşteri Seçimi" ekranı gelir.
    *   **Akıllı Arama:** İsmin baş harfiyle DB'den müşteri bulur (`react-select`).
    *   **Mail:** Kayıtlı mail otomatik gelir. Yoksa elle giriş **ZORUNLUDUR**.

3.  **Satış Tamamlama & Backend (Python):**
    *   "Satışı Onayla" butonuna basılır.
    *   **Adım A (Stok):** DB'de stok düşülür (`-1`).
    *   **Adım B (PDF & QR):** Python `reportlab` ile anlık PDF fiş oluşturulur. Fiş üzerine `ARAS-SALE-{UUID}` formatında QR kod basılır.
    *   **Adım C (Mail):** Oluşan PDF, müşterinin mail adresine gönderilir (SMTP/Resend).

## 3.3. İade Modu (Return Flow)
Saha personelinin ana ekranında iki büyük buton bulunur: **🟢 SATIŞ YAP** ve **🔴 İADE AL**.

**İade Senaryosu:**
1.  **Giriş:** "🔴 İADE AL" butonuna basılır.
2.  **Tarama:** Müşterinin elindeki fişteki QR kod (`ARAS-SALE-...`) kamera ile taranır.
3.  **Doğrulama:**
    *   Sistem `Sale_ID`'yi veritabanında sorgular.
    *   Daha önce iade edilmiş mi? (`status` kontrolü).
    *   Satış gerçek mi?
4.  **Onay:**
    *   Satış detayları (Ürün, Tarih, Tutar) ekrana gelir.
    *   "İadeyi Tamamla" denildiğinde:
        *   Stok artar (`+1`).
        *   Satış durumu `İade Edildi` olarak güncellenir.
        *   Müşteriye "İade Gider Pusulası" mail atılır.

## 4. Veritabanı ve İzolasyon Stratejisi (Kritik)
Ana veritabanını bozmamak ve dashboard raporlarını kirletmemek için **"Gölge Tablo"** stratejisi uygulanacaktır.

1.  **`pos_sales` Tablosu (Yeni & İzole):**
    *   Gerçek `sales` tablosuna dokunulmaz. Tüm POS satışları buraya kaydedilir.
    *   Kolonlar: `id`, `product_id`, `quantity`, `total_price`, `qr_code` (UUID), `status` (completed/returned), `customer_email`, `pdf_url`.
    *   **Dashboard Etkisi:** Sıfır. Yönetim paneli bu tabloyu görmez.

2.  **`pos_carts` Tablosu (Yeni):**
    *   Sepet verisinin kalıcılığı için. (Müşteri vazgeçerse veya internet koparsa veri kaybını önlemek için).

3.  **Simülasyon Mağazası ve Stok (Inventory):**
    *   Stok düşüşlerini göstermek zorundayız, ancak gerçek mağazaların (Store ID: 1-5) stoklarını bozmak istemiyoruz.
    *   **Çözüm:** `stores` tablosunda **ID: 9999** olan özel bir **"DEMO POS MAĞAZASI"** oluşturulacak.
    *   Tüm POS işlemleri bu mağaza üzerinden yapılacak. Böylece ana raporlar filtreleme ile (`WHERE store_id != 9999`) temiz kalacak.



## 3. UI/UX Tasarımı ve Mobil (PWA) Düzeni
*   **Tasarım Felsefesi:** Mobile-First (Önce Mobil). TailwindCSS `md:` breakpoint'i ile masaüstüne genişleme.
*   **Masaüstü (Desktop) Görünümü:**
    *   **Düzen:** İki Sütunlu (Split View).
    *   **Sol Panel (%60):** Ürün Listesi (Grid/Table), Arama Çubuğu.
    *   **Sağ Panel (%40):** Sepet Özeti, Hızlı Tuşlar (Nakit, Kredi Kartı), Büyük "Öde" Butonu.
*   **Mobil (Mobile) Görünümü:**
    *   **Header:** Minimalist. Sadece Geri Dön (Back), Mağaza İsmi ve Bağlantı Durumu. Menü gizlenir.
    *   **İçerik:** Dikey kaydırılabilir ürün listesi. Kartlar dokunmatik dostu (min-height: 60px).
    *   **Bottom Action Bar (Sabit Alt Menü):**
        *   **Sol:** Toplam Tutar (Vurgulu).
        *   **Sağ:** "ÖDE" Butonu (Tam Genişlik veya Büyük Buton).
        *   **FAB (Yüzen Buton):** "Kamera/QR Tara" (Erişimi kolay sağ alt köşe).
    *   **Etkileşimler:** Sepet ürününü sola kaydırarak silme (Swipe-to-Delete).

## 5. UI/UX Tasarım Spesifikasyonları (Figma İncelemesi Sonrası)
Kullanıcının ilettiği Figma taslağı ("Login -> Seçim -> Kasa -> Satış") referans alınarak, projenin mevcut **"Modern Dark / Glassmorphism"** temasına uygun hale getirilecektir.

### 5.1. Renk Paleti ve Tema
*   **Zemin:** `bg-slate-900` (Derin, profesyonel koyu mod).
*   **Paneller:** `bg-slate-800/50 backdrop-blur-xl` (Cam efekti).
*   **Vurgu (Accent):** `blue-600` (Butonlar, Aktif Durumlar), `green-500` (Onay/Başarılı), `amber-500` (Uyarı/Offline).
*   **Metin:** `text-slate-200` (Okunabilirlik için yumuşak beyaz).

### 5.2. Kasa Ekranı Düzeni (POS Layout)
Ekran yatayda iki ana bloğa ayrılacaktır (Masaüstü için):
1.  **Sol Panel (Katalog & Tarama - %65):**
    *   **Üst Bar:** Geniş "Ürün Ara (İsim/Barkod)" input alanı. Yanında "Kamera Aç" butonu.
    *   **Grid Alanı:** Ürün kartları (Görsel, İsim, Fiyat, Stok Durumu).
    *   **Kamera Modu:** Kamera açıldığında Grid'in üstünde veya modal olarak canlı önizleme.
2.  **Sağ Panel (Sepet & İşlem - %35):**
    *   **Liste:** Eklenen ürünler (Satır bazında: İsim, Adet Artır/Azalt, Tutar, Sil).
    *   **Alt Özet:** Ara Toplam, KDV, **GENEL TOPLAM**.
    *   **Aksiyon Butonları:**
        *   `İptal` (Sepeti Temizle - Gri).
        *   `Satışı Tamamla` (Ödeme Modalını Aç - Yeşil/Mavi Gradient).

### 5.3. Satış Tamamlama Modalı (Checkout)
Basit bir modal yerine, adım adım ilerleyen bir yapı:
1.  **Müşteri Bilgisi (Opsiyonel):** "İsim / E-posta" (Hızlı seçim veya yeni giriş).
2.  **Ödeme Tipi:** Nakit / Kredi Kartı / Cari.
3.  **Onay:** Dijital Fiş Gönderimi (E-posta/SMS placeholder).

## 6. Demo Verisi Hazırlığı
Sunum sırasında barkod okuyucuyu (veya hızlı klavye girişini) test etmek için sabit ürünler:
*   `869001` -> Laptop (Premium)
*   `869002` -> Telefon (X-Pro)
*   `869003` -> Kulaklık

## 4. Test ve Doğrulama Adımları
1.  **Normal Satış:** Ürün okut -> Satışı Bitir -> "Başarılı" mesajını gör.
2.  **Offline Senaryosu:**
    *   Bilgisayarın Wi-Fi bağlantısını kes.
    *   Ürün okut -> Satışı Bitir.
    *   Uyarı: "İnternet Yok! Kuyruğa Eklendi (Sarı)".
3.  **Sync Senaryosu:**
    *   Wi-Fi'yi geri aç.
    *   Sistemin otomatik olarak "Veriler Buluta Yüklendi (Yeşil)" mesajını verdiğini gör.
4.  **Hardware Senaryosu:**
    *   Barkod okuyucu (veya hızlı copy-paste) ile seri ürün girişi yap.
    *   Sistemin takılmadan ürünleri eklediğini doğrula.
