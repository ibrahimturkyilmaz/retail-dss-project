# Proje Geri Yükleme ve Kurulum Kılavuzu (Format Sonrası)

Bilgisayarınıza format attıktan sonra bu projeyi tekrar çalışır hale getirmek için aşağıdaki adımları sırasıyla uygulayın.

## 1. Ön Hazırlıklar

### Gerekli Yazılımlar
*   **Git**: [İndir ve Kur](https://git-scm.com/downloads)
*   **Python 3.11.5**: [İndir ve Kur](https://www.python.org/downloads/release/python-3115/) (Kurulumda "Add Python to PATH" seçeneğini işaretlemeyi UNUTMAYIN!)
*   **Node.js (LTS sürümü)**: [İndir ve Kur](https://nodejs.org/) (Frontend için gerekli)
*   **VS Code**: (Önerilen editör)

## 2. Projeyi İndirme (Clone)

Terminali (Komut İstemi veya PowerShell) açın ve projeyi masaüstüne indirin:

```bash
cd Desktop
git clone https://github.com/ibrahimturkyilmaz/retail-dss-yedek.git
cd retail-dss-yedek
```

## 3. Backend (Python) Kurulumu

### Sanal Ortam Oluşturma
Backend bağımlılıklarını izole etmek için yeni bir sanal ortam oluşturun:

```bash
cd backend
python -m venv venv
```

### Sanal Ortamı Aktifleştirme
**Windows için:**
```bash
.\venv\Scripts\activate
```

### Kütüphanelerin Yüklenmesi
```bash
pip install -r requirements.txt
```

### Veritabanını Oluşturma
Proje `retail.db` dosyasını içermemektedir (yedekleme dışı bırakıldı). Veritabanını sıfırdan oluşturmak ve örnek verilerle doldurmak için:

```bash
python seed.py
```
*(Bu işlem `retail.db` dosyasını oluşturacak ve mağaza/ürün verilerini ekleyecektir.)*

### Backend'i Başlatma
Hala `backend` klasöründeyken:
```bash
uvicorn main:app --reload --port 8001
```
Terminalde "Application startup complete" yazısını gördüğünüzde backend çalışıyor demektir. (Bu terminali kapatmayın!)

## 4. Frontend (React) Kurulumu

Yeni bir terminal penceresi açın ve projenin ana klasörüne gidin:

```bash
cd retail-dss-yedek
cd frontend
```

### Paketleri Yükleme
```bash
npm install
```

### Frontend'i Başlatma
```bash
npm run dev
```
Terminalde verilen "Local: http://localhost:5173" adresine tıklayarak uygulamayı tarayıcıda açabilirsiniz.

## Özet Komut Listesi

**Backend:**
1. `cd backend`
2. `python -m venv venv`
3. `.\venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. `python seed.py`
6. `uvicorn main:app --reload --port 8001`

**Frontend:**
1. `cd frontend`
2. `npm install`
3. `npm run dev`

İyi çalışmalar!
