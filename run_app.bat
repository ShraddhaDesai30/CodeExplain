@echo off
cd /d "%~dp0"
if not exist venv\Scripts\python.exe (
  py -m venv venv
  if errorlevel 1 pause & exit /b 1
)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
pause
