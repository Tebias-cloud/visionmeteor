@echo off
echo =======================================
echo 🛰️  Iniciando VisionMeteor Full-Stack
echo =======================================

echo.
echo Iniciando el Servidor Backend (Python/FastAPI)...
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
start "VisionMeteor Backend" cmd /k "chcp 65001 >nul && cd backend && python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload"

echo Iniciando el Dashboard (Next.js)...
start "VisionMeteor Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo =======================================
echo ✅ Servicios Iniciados.
echo 🌍 Dashboard interactivo: http://localhost:3000
echo ⚙️ API de Python: http://localhost:8000
echo =======================================
echo Nota: Cierra las dos ventanas emergentes de CMD para detener los servidores.
pause
