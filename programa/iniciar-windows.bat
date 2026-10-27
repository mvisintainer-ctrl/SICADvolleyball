@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  py -3.10 -m venv .venv
  if errorlevel 1 (
    echo Instale o Python 3.10 de 64 bits de https://www.python.org/downloads/windows/
    pause
    exit /b 1
  )
)
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
  pause
  exit /b 1
)
.venv\Scripts\python.exe -m app.main
if errorlevel 1 pause
