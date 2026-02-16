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

## 4. Uygulama Akışı (Saha Operasyonu)
1.  **Giriş:** Saha personeli mobil cihazdan giriş yapar.
2.  **SAHA Sekmesi:** Alt menüden "SAHA" (Barkod) ikonuna tıklar.
3.  **Okutma:** Kamera açılır (veya Bluetooth okuyucu kullanılır).
4.  **Satış:** Ürünler sepete eklenir.
5.  **Offline:** İnternet kesilse bile satış tamamlanır, `syncService` veriyi saklar.
6.  **Fiş:** Müşteriye QR kod gösterilir veya PDF gönderilir.


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

## 4. Demo Verisi Hazırlığı
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
