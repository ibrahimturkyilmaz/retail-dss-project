@echo off
echo --- RetailDSS Hizli Deploy Araci ---
echo.

set /p msg="Commit mesaji girin (Varsayilan: update): "
if "%msg%"=="" set msg=update

echo.
echo [1/3] Dosyalar ekleniyor (git add)...
git add .

echo [2/3] Commit aliniyor (git commit)...
git commit -m "%msg%"

echo [3/3] GitHub'a gonderiliyor (git push)...
git push origin main

echo.
echo ✅ Islem tamam!
echo 🚀 Render (Backend) ve Vercel (Frontend) otomatik deploy baslatacak.
echo.
pause
