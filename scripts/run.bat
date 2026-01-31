@echo off
TITLE AdminOS Launcher

:: Vai para a raiz do projeto (volta um nível)
cd ..

echo ==================================================
echo 🚀 INICIANDO ADMIN OS (MODO WINDOWS)
echo ==================================================
echo.

:: Agora estamos na raiz, o resto funciona igual
if not exist "backend\venv" (
    echo [ERRO] A pasta 'venv' nao foi encontrada no backend.
    pause
    exit
)

echo [1/2] Ligando API (Python/FastAPI)...
start "AdminOS - Backend API" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload --port 8000"

echo [2/2] Ligando Interface (Vue.js)...
cd frontend
npm run dev