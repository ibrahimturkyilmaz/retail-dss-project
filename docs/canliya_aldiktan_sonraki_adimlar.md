# 🚀 Canlıya Aldıktan Sonraki Adımlar (Next Level Roadmap)

Bu belge, RetailDSS projesinin bulut mimarisine geçişinden sonraki (Post-Deployment) büyüme stratejisini ve teknik yol haritasını içerir.

---

## 🟢 Aşama 1: Kullanıcı ve Veri Kalıcılığı (Hemen Yapılabilir)
**Mevcut Durum:**
Şu an AI sohbet geçmişi ve ayarlar tarayıcının hafızasında (LocalStorage) duruyor. Bu, verilerin cihazlar arasında senkronize olmasını engelliyor.

**Ne Yapacağız?**
- `chat_history` ve `user_preferences` tablolarını Supabase'e ekleyeceğiz.
- Mevcut `useAuth` context'ini güncelleyerek bu verileri veritabanından çekmesini sağlayacağız.

**Beklenen Sonuç:**
- Bilgisayarda başladığın sohbeti telefondan (mobil siteden) devam ettirebileceksin.
- "Favori Raporlarım" ve tema tercihleri her cihazda aynı kalacak.
- Tamamen kişiselleştirilmiş bir deneyim sunulacak.

---

## 🟡 Aşama 2: Gerçek Zamanlı (Real-Time) Etkileşim
**Mevcut Durum:**
Verilerin güncellenmesi için sayfanın yenilenmesi gerekiyor.

**Ne Yapacağız?**
- Supabase'in "Realtime" özelliğini aktif edeceğiz.
- Stok tablosuna (`stocks`) bir "Listener" (Dinleyici) ekleyeceğiz.

**Senaryo:**
Mağaza müdürü A, bir ürünü sattığında, Merkez Ofis dashboard'unda sayfa yenilemeye gerek kalmadan stok sayısı anında düşecek ve grafik güncellenecek.

**Beklenen Sonuç:**
- Canlı borsa ekranı gibi yaşayan, dinamik bir dashboard.
- Operasyonel hızda %100 artış.

---

## 🔴 Aşama 3: Forecasting 2.0 (Yapay Zeka Devrimi)
**Mevcut Durum:**
Şu an Facebook Prophet kullanıyoruz. Mevsimsellik başarısı yüksek ancak karmaşık dış faktörleri (etkinlikler, ani hava değişimi, ekonomik veriler) tam olarak modelleyemiyoruz.

**Ne Yapacağız?**
- **XGBoost** veya **LightGBM** modellerine geçeceğiz.
- Feature Engineering (Öznitelik Mühendisliği) ile daha fazla veri besleyeceğiz.

**Farkı Ne?**
"Hafta sonu yağmur yağarsa şemsiye satışı %15 artar ama AVM'ye giden azalır" gibi çok karmaşık, lineer olmayan ilişkileri öğrenebilir.

**Beklenen Sonuç:**
- %95+ doğrulukta satış tahminleri.
- Stok maliyetlerinde ciddi düşüş (daha az atıl stok).

---

## 🟣 Aşama 4: Mobil Uygulama (PWA)
**Mevcut Durum:**
Sadece web tarayıcısı üzerinden erişiliyor.

**Ne Yapacağız?**
- Frontend'e `manifest.json` ve `service worker` ayarları ekleyeceğiz.
- Siteyi "Uygulamayı Yükle" butonuyla telefona indirilebilir hale getireceğiz.

**Beklenen Sonuç:**
- App Store'a koymaya gerek kalmadan, native uygulama gibi çalışan bir mobil uygulama.
- Çevrimdışı (Offline) çalışma yeteneği.
- Ana ekrana ikon olarak eklenebilme.
