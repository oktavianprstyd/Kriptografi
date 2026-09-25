@echo off
echo ========================================================
echo Membuka Aplikasi Kriptografi (UPN Veteran Yogyakarta)
echo ========================================================
cd /d "%~dp0"
python -m streamlit run app.py
pause
