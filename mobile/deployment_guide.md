# Proje Yayınlama Kılavuzu (Deployment Guide)

Bu proje statik bir web uygulaması olduğu için (**Vite + React**), herhangi bir statik hosting servisinde kolayca yayınlanabilir.

## Yöntem 1: GitHub Pages (Otomatik)

Proje içine eklediğimiz `.github/workflows/deploy.yml` dosyası sayesinde, kodunuzu GitHub'a yüklediğinizde otomatik olarak yayınlanacaktır.

### Adımlar:
1.  **GitHub Deposu Oluşturun:** GitHub hesabınızda yeni bir repo açın.
2.  **Kodu Yükleyin:**
    ```bash
    git init
    git add .
    git commit -m "İlk kurulum"
    git branch -M main
    git remote add origin https://github.com/KULLANICI_ADI/REPO_ADI.git
    git push -u origin main
    ```
3.  **Ayarları Kontrol Edin:**
    *   Repo sayfanızda **Settings > Pages** sekmesine gidin.
    *   **Source** kısmında "GitHub Actions" seçeneğinin seçili olduğundan emin olun (veya bazen otomatiktir).
    *   Birkaç dakika içinde "Build" işlemi biter ve size sitenizin linkini verir (örneğin: `https://kullaniciadi.github.io/repo-adi/`).

## Yöntem 2: Vercel (Önerilen Alternatif)

Vercel, React projeleri için optimize edilmiştir ve kurulumu çok basittir.

### Adımlar:
1.  [Vercel.com](https://vercel.com) adresine gidin ve GitHub ile giriş yapın.
2.  "Add New > Project" butonuna tıklayın.
3.  GitHub reponuzu seçin ve "Import" deyin.
4.  Hiçbir ayarı değiştirmenize gerek yok. **"Deploy"** butonuna basmanız yeterli.
5.  Siteniz anında yayına girer.

## Yöntem 3: Netlify (Manuel / Sürükle-Bırak)

Kodla uğraşmak istemiyorsanız:
1.  Bilgisayarınızda projeyi derleyin: `npm run build`
2.  Proje klasöründe oluşan `dist` klasörünü bulun.
3.  [Netlify Drop](https://app.netlify.com/drop) sayfasına gidin.
4.  `dist` klasörünü sayfaya sürükleyip bırakın.
5.  Siteniz yayında!

---

**Not:** Veritabanı verileri şu an proje içinde (`src/data` vb.) statik olarak tutulduğu için, verileri güncellemek istediğinizde MS SQL'den yeni JSON çıktısı alıp koda eklemeniz ve tekrar `push` etmeniz yeterlidir.
