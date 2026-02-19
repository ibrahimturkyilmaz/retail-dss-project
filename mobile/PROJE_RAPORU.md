# Bitirme Projesi Teknik Raporu

## 1. Giriş
Bu çalışma, perakende sektörü için geliştirilmiş, konum tabanlı servisler (LBS) ile entegre, modern bir mobil web uygulamasının (PWA) tasarımını ve uygulamasını konu almaktadır. Çalışmanın temel amacı, kullanıcının coğrafi konum verilerini işleyerek (Geofencing), mağaza içi ve mağaza yakını senaryoları için özelleştirilmiş, gerçek zamanlı etkileşimler sunmaktır.

---

## 2. Materyal ve Yöntem

### 2.1. Ön Yüz Mimarisi (Frontend Architecture): **React.js**
Uygulamanın kullanıcı arayüzü katmanında, bileşen tabanlı (component-based) yapısı ve Sanal DOM (Virtual DOM) mimarisi nedeniyle **React.js** kütüphanesi tercih edilmiştir.
*   **Gerekçe:** Modern web uygulamalarında modülerlik ve yeniden kullanılabilirlik (reusability) esastır. React, deklaratif programlama paradigması ile karmaşık kullanıcı arayüzlerinin yönetimini ve durum (state) değişimlerinin optimizasyonunu sağlamaktadır.
*   **Literatürdeki Alternatifleri:** Vue.js ve Angular. React'in tercih edilme sebebi, geniş ekosistemi ve React Native aracılığıyla mobil platformlara (Cross-Platform) dönüştürülebilirliğinin yüksek olmasıdır.

### 2.2. Derleme ve Geliştirme Altyapısı: **Vite**
Geleneksel paketleyicilerin (Webpack) getirdiği performans maliyetlerini minimize etmek amacıyla, Native ES Modülleri (ESM) tabanlı **Vite** derleme aracı kullanılmıştır.
*   **Avantajları:** Anlık Modül Değişimi (HMR) özelliği sayesinde geliştirme sürecindeki geri bildirim döngüsü milisaniyeler seviyesine indirilmiştir.

### 2.3. Kullanıcı Arayüzü ve Deneyimi (UI/UX): **Tailwind CSS & Framer Motion**
Tasarım dili olarak, "Utility-First" yaklaşımını benimseyen **Tailwind CSS** kullanılmıştır. Bu yaklaşım, CSS dosya boyutunu (bundle size) minimize ederken, tutarlı bir tasarım sistemi oluşturulmasına olanak tanır.
*   **Etkileşim:** Mobil uygulama hissiyatını (Native Feel) artırmak amacıyla, fizik tabanlı animasyon kütüphanesi olan **Framer Motion** entegre edilmiştir.

### 2.4. Dağıtım ve DevOps (CI/CD): **GitHub Pages & Actions**
Projenin sürekli entegrasyonu ve dağıtımı (CI/CD) için **GitHub Actions** altyapısı kurulmuştur.
*   **Otomasyon:** Ana koda (main branch) yapılan her güncelleme (`push`), otomatik olarak bir derleme (build) süreci başlatır.
*   **Hosting:** Derlenen statik dosyalar, **GitHub Pages** üzerinde ücretsiz ve güvenli (HTTPS) bir şekilde barındırılarak son kullanıcının erişimine sunulur. Bu yapı, sunucu maliyetini ortadan kaldırır ve yüksek erişilebilirlik sağlar.

---

## 3. Konum Tabanlı Servisler (Location Based Services)

### 3.1. Coğrafi Konumlandırma Protokolü: **HTML5 Geolocation API**
Kullanıcının anlık konumunun tespiti için W3C standardı olan **HTML5 Geolocation API** kullanılmıştır.
*   **Metodoloji:** IP tabanlı konumlandırmanın aksine; GPS, Wi-Fi ve baz istasyonu verilerini hibrit işleyen `navigator.geolocation` arayüzü tercih edilmiştir.

### 3.2. Geofencing ve Bildirim Yönetimi
Kullanıcının belirli bir coğrafi alana (mağaza çevresi) girmesi durumunda tetiklenen bildirim mekanizmasıdır.
*   **Uygulama:** Her 5 saniyede bir kullanıcının konumu ile hedef noktalar arasındaki mesafe "Haversine Formülü" ile hesaplanır. Mesafe belirlenen yarıçapın (örn. 500m) altına düştüğünde kullanıcıya görsel bildirim (`NotificationOverlay`) gösterilir.

---

## 4. Yazılım Mimarisi ve Veri Yönetimi

### 4.1. Durum Yönetimi Stratejisi (State Management): **Context API**
Uygulamanın veri akışı, React'in yerleşik **Context API** mekanizması üzerine kurgulanmıştır.
*   **UserContext:** Kullanıcı profil ve tercihlerin yönetimi. (Veriler `localStorage` tabanlı kalıcı hale getirilmiştir)
*   **LocationContext:** GPS verileri, izin durumları ve geofence tetikleyicilerinin merkezi yönetimi.
*   **Kalıcılık (Persistence):** Sepet ve Favori verileri tarayıcının yerel hafızasına (Local Storage) anlık olarak kaydedilir. Bu sayede sayfa yenilense bile kullanıcı verileri kaybolmaz.

### 4.2. Servis Yönelimli Katman (Service Layer)
İş mantığı (Business Logic) ile sunum katmanı (Presentation Layer) birbirinden izole edilmiştir. `src/data/mockData.js` üzerinde tanımlı simüle edilmiş veri seti kullanılarak, gerçek bir backend mimarisine gerek kalmadan uygulamanın tüm fonksiyonları (Sepet, Favoriler, Listeleme) istemci tarafında çalıştırılmaktadır.
*   **Avantajı:** Sunucu bağımlılığı olmadığı için uygulama GitHub Pages gibi statik sunucularda %100 performansla çalışır ve kesinti yaşanmaz.

---

## 5. Proje Klasör Yapısı (Folder Structure)

Projenin kaynak kodları, sürdürülebilirlik ilkeleri gözetilerek modüler bir yapıda (Screens, Components, Contexts, Services) düzenlenmiştir.

---

## 6. Proje Yol Haritası ve İlerleme Durumu: "Önce Güvenlik, Sonra Şov"

Projenin geliştirilme sürecinde, bitirme projesi teslim kuralları ve risk yönetimi göz önüne alınarak **"Hibrit / Aşamalı"** bir strateji benimsenmiştir. Bu strateji, projenin her aşamada "sunulabilir" ve "çalışır" durumda olmasını garanti altına alır.

### AŞAMA 1: Güvenli Liman (Tamamlandı - Mevcut Durum)
Uygulamanın en kararlı ve risksiz versiyonudur. İstemci taraflı (Client-Side) mimari ile %100 performans hedeflenmiştir.

**Bu Aşamada Geliştirilebilecek Ek Özellikler:**
Mevcut mimari (Aşama 1) bozulmadan şu özellikler eklenebilir:
*   **PWA Kurulumu:** Kullanıcıya "Ana Ekrana Ekle" butonu sunularak uygulamanın yerel bir uygulama gibi yüklenmesi.
*   **Gelişmiş Filtreleme:** İstemci tarafında (Client-side) çalışan, renk, beden ve fiyat aralığına göre anlık filtreleme.
*   **Karanlık Mod (Dark Mode):** Tailwind CSS altyapısı kullanılarak sisteme duyarlı tema desteği.
*   **Yapay Zeka (Mock AI):** "Bunu beğenenler bunu da aldı" gibi senaryolar için daha akıllı sahte veri setleri oluşturulması.

### AŞAMA 2: Bulut Entegrasyonu (Orta Vade - Bonus Hedef)
Projenin "Statik" yapısından "Dinamik" yapıya geçiş evresidir. Bu aşamada sunucu maliyeti olmadan **Firebase (Backend-as-a-Service)** teknolojileri entegre edilir.

**Detaylı Plan:**
1.  **Authentication (Kimlik Doğrulama):** Mevcut sahte giriş yerine, **Firebase Auth** kullanılarak Google, Apple ve E-posta ile gerçek kullanıcı yönetimi.
2.  **Firestore (Gerçek Zamanlı Veritabanı):**
    *   Sepet ve Favori verilerinin buluta taşınarak, kullanıcının mobilden eklediği ürünü web tarayıcısında da görmesi (Cihazlar arası senkronizasyon).
    *   Basit stok takibi mantığının veritabanına işlenmesi.
3.  **Hosting:** GitHub Pages yerine Firebase Hosting kullanılarak daha hızlı CDN (Content Delivery Network) desteği.

### AŞAMA 3: Kurumsal Ölçekleme (Uzun Vade - Gelecek Vizyonu)
Projenin bir bitirme ödevinden çıkıp, ticari bir "Startup" ürününe dönüşmesi durumunda uygulanacak mimari değişikliklerdir.

**Detaylı Dönüşüm Planı:**
1.  **Microservices Mimarisi:**
    *   Tek parça (Monolithic) yapı yerine; Ürün Servisi, Sipariş Servisi, Bildirim Servisi gibi ayrıştırılmış **Node.js/Go** servisleri.
    *   Bu servislerin **Docker** konteynerleri içinde izole edilmesi ve **Kubernetes** ile yönetilmesi.
2.  **Veritabanı Dönüşümü:**
    *   İlişkisel verilerin (Sipariş-Fatura) tutarlılığı için **PostgreSQL** gibi güçlü bir SQL veritabanına geçiş.
    *   Ürün katalogları ve loglama için **MongoDB** veya **Elasticsearch** kullanımı.
3.  **Ödeme ve Lojistik:**
    *   **Iyzico / Stripe** API entegrasyonu ile gerçek kredi kartı işlemleri.
    *   Kargo firmalarının API'ları ile sipariş takip entegrasyonu.
4.  **AI/ML Destekli Öneri Motoru:**
    *   Kullanıcının gezinme geçmişini analiz eden ve Python (TensorFlow/PyTorch) tabanlı çalışan gerçek bir öneri algoritması entegrasyonu.

---
**Rapor Tarihi:** 2 Ocak 2026
**İlk Rapor Tarihi:** 18 Aralık 2025
