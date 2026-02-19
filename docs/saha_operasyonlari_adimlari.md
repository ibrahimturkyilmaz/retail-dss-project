# POS Sistemi Saha Operasyonları Adımları (Field Operations Steps)

Bu doküman, POS sisteminin sahadan veri toplama, işleme ve raporlama süreçlerinin teknik uygulama planını içerir.

## FAZ 1: Veritabanı Altyapısı (Database Infrastructure)
Veritabanı izolasyonu için gerekli tabloların oluşturulması.

*   **`models.py` Güncellemesi:**
    *   `PosSale`: Satış başlık bilgileri (Fiş No, Tutar, Tarih).
    *   `PosSaleItem`: Satış detayları (Ürün, Adet, Fiyat).
    *   `PosPayment`: Ödeme detayları (Nakit, Kredi Kartı).
    *   `PosZReport`: Gün sonu raporları.
*   **Kontrol Noktası:** Tabloların veritabanında başarıyla oluşturulduğunun teyidi.

## FAZ 2: Veri Giriş Kapısı (Ingestion API)
POS cihazlarından gelen verilerin karşılanması.

*   **Endpoint:** `POST /api/pos/sync`
*   **Güvenlik:**
    *   **Idempotency:** Aynı `receipt_no` ile gelen mükerrer isteklerin reddedilmesi.
    *   **Validasyon:** Eksik veya hatalı veri formatlarının kontrolü.
*   **Kontrol Noktası:** Test verisi ile API'nin başarılı yanıt vermesi ve verinin `pos_sales` tablosuna yazılması.

## FAZ 3: İşleme Motoru (Processing Engine)
Staging tablolarındaki verilerin ana sisteme aktarılması.

*   **Modül:** `sync_engine.py`
*   **İş Mantığı:**
    *   **SATIŞ (SALE):** Ana stoktan (`Inventory`) adet düşülmesi.
    *   **İADE (RETURN):** Ana stoğa (`Inventory`) adet eklenmesi.
    *   **HATA YÖNETİMİ:** Tanımsız ürün (Missing SKU) durumunda kaydın `ERROR` statüsüne alınması.
*   **Kontrol Noktası:** Satış yapıldığında stok miktarının otomatik olarak azaldığının doğrulanması.

## FAZ 4: Frontend & Zaman Yolculuğu (Time Simulation)
Gün sonu işlemlerinin güvenli testi için zaman simülasyonu.

*   **TimeContext:** Uygulama genelinde 'Sanal Saat' kullanımı.
*   **TimeTravelWidget:** Geliştiriciler için saati ileri/geri alma aracı.
*   **Z-Raporu Butonu:** Sadece kapanış saatinden sonra (örn: 19:00) görünür olması.
*   **Kontrol Noktası:** Saati 20:00'ye aldığımızda Z-Raporu butonunun görünür hale gelmesi.

## FAZ 5: Raporlama ve Mail (SMTP)
Gün sonu raporunun e-posta ile gönderilmesi.

*   **SMTP Entegrasyonu:** Gerçek mail sunucusu (Gmail, Outlook vb.) ayarları.
*   **Mail İçeriği:** Günlük ciro, nakit/kredi kartı dağılımı, iade toplamları.
*   **Kontrol Noktası:** Kullanıcının kendi mail adresine gerçek bir Z-Raporu e-postası düşmesi.
