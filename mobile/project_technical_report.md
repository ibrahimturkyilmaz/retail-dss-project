# Proje Teknik Raporu ve Geliştirme Özeti

Bu rapor, "Perakende Mobil Uygulama Demosu" projesi boyunca izlenen, kullanılan teknolojileri, yöntemleri ve alınan stratejik kararları belgeler.

---

## 🏗️ 1. Mimari ve Teknoloji Yığını (Architecture & Tech Stack)

### Frontend (Ön Yüz)
*   **React (Vite):** Hızlı geliştirme süreci ve modern JavaScript özellikleri için seçildi. Create React App'e göre daha hafif ve hızlıdır.
*   **TailwindCSS:** Stil yönetimi için Utility-first yaklaşımı. Hızlı prototipleme ve tutarlı tasarım sistemi sağladı. "Premium" hissi için özel renk paletleri ve shadow efektleri tanımlandı.
*   **Framer Motion:** Animasyonlar için. Sayfa geçişleri, Story modu dönme efektleri ve Skeleton yükleme ekranlarında akıcılık sağlamak için kullanıldı.
*   **Context API:** Durum yönetimi (State Management). Proje orta ölçekli olduğu için Redux gibi ağır kütüphaneler yerine React'in kendi `UserContext`, `CartContext`, `LocationContext` yapıları tercih edildi.

### Backend (Arka Yüz)
*   **Node.js & Express:** JavaScript tabanlı olduğu için frontend ile dil bütünlüğü sağladı. Hafif ve hızlı Request/Response döngüsü sunduğu için tercih edildi.
*   **MSSQL (Microsoft SQL Server):** Mevcut perakende veritabanı yapısına (Customers, Products, Stores) entegre olmak için seçildi.
*   **Native Driver (`mssql`):** ORM (Prisma/TypeORM) yerine performans ve doğrudan SQL kontrolü için native sürücü kullanıldı.

### Dağıtım (Deployment)
*   **Frontend:** GitHub Pages (Statik site barındırma).
*   **Backend Bağlantısı:** Ngrok (Tünelleme).
*   **Neden?** Local SQL Server'ı buluta taşımak (Azure SQL/AWS RDS) maliyetli ve karmaşık olacağı için, demo amacıyla local portu internete açan Ngrok stratejisi benimsendi.

---

## 🛠️ 2. Uygulanan Metodolojiler ve Kritik Özellikler

### Konum Servisi (Geolocation Strategy)
*   **Sorun:** Tarayıcıların "Permissions API" desteği tutarsızdı ve konum izni penceresi bazen açılmıyordu.
*   **Çözüm:** `navigator.permissions` yerine doğrudan kullanıcı etkileşimiyle tetiklenen (`getCurrentPosition`) ve zaman aşımı (Timeout) mekanizması içeren sağlam (Robust) bir yapı kuruldu.
*   **UI Geri Bildirimi:** Konum alınırken dönen spinner ve hata durumunda (GPS kapalı vs.) özel alert mekanizmaları eklendi.

### Kullanıcı Deneyimi (UX) İyileştirmeleri
*   **Skeleton Loading:** Veri yüklenirken boş sayfa göstermek yerine, gri kutucukların dalgalandığı "Skeleton" yapısı kurularak algılanan hız (Perceived Performance) artırıldı.
*   **Story Modu:** Kategoriler, Instagram hikayeleri gibi dairesel ve gradyanlı hale getirilerek modern bir görünüm sağlandı. "Live" kategorisi için özel animasyon eklendi.
*   **Oyunlaştırma (Gamification):** Profil sayfasına "2 sipariş daha ver, seviye atla" gibi motive edici metinler eklendi.

---

## 🔄 3. Alternatif Yöntemler ve Neden Seçilmedi?

### A. Veritabanı
*   **Alternatif:** Firebase / MongoDB (NoSQL).
*   **Neden Seçilmedi?** Projenin amacı, mevcut SQL Server verisini mobile taşımaktı. NoSQL dönüşümü veri tutarlılığını zorlaştırırdı.

### B. Backend Dağıtımı
*   **Alternatif:** Render.com veya Vercel Functions.
*   **Neden Seçilmedi?** Bulut sunucuların (Render), sizin bilgisayarınızdaki yerel SQL Server'a (`localhost`) erişmesi için VPN veya Statik IP gerekirdi. Bu, demo süreci için aşırı karmaşıktı. Ngrok en pratik çözümdü.

### C. Stil
*   **Alternatif:** Bootstrap / Material UI.
*   **Neden Seçilmedi?** Bu kütüphaneler çok "standart" ve hazır şablon gibi hissettiriyor. TailwindCSS ile tamamen özgün ve markaya özel "Boutique" bir tasarım dili oluşturuldu.

---

## 🚀 4. Canlı Öncesi Son Durum
Şu an proje **"Production Ready" (Yayına Hazır)** seviyesine yakındır.

*   ✅ **Login:** Gerçek veritabanı sorgusu ile çalışıyor.
*   ✅ **Ürünler:** SQL'den filtrelenerek geliyor.
*   ✅ **Sepet & Favoriler:** Local state üzerinde kusursuz çalışıyor.
*   ✅ **Arayüz:** Responsive, modern ve animasyonlu.

**Öneri:** Bir sonraki aşamada, Sepet verisini de veritabanına yazarak (`Carts` tablosu) kullanıcı uygulamayı silse bile sepetinin kalıcılığını sağlamak olabilir.
