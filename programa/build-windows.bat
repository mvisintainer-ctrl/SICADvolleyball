@echo off
setlocal
cd /d "%~dp0"
py -3.10 --version >nul 2>&1
if errorlevel 1 (
  echo Para recompilar esta edicao, instale Python 3.10 de 64 bits.
  pause
  exit /b 1
)
if not exist .venv\Scripts\python.exe py -3.10 -m venv .venv
if errorlevel 1 exit /b 1
.venv\Scripts\python.exe -m pip install -r requirements-build.txt
if errorlevel 1 exit /b 1
.venv\Scripts\python.exe build_windows.py
if errorlevel 1 exit /b 1
echo Executavel criado em dist\SICADvolleyball.exe
pause
