@echo off
TITLE AdminOS Launcher

echo ==================================================
echo 🚀 INICIANDO ADMIN OS (MODO WINDOWS)
echo ==================================================
echo.

:: 1. Verifica se a venv existe
if not exist "backend\venv" (
    echo [ERRO] A pasta 'venv' nao foi encontrada no backend.
    echo Por favor, entre na pasta backend e rode: python -m venv venv
    pause
    exit
)

:: 2. Inicia o BACKEND em uma nova janela
echo [1/2] Ligando API (Python/FastAPI)...
start "AdminOS - Backend API" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload --port 8000"

:: 3. Inicia o FRONTEND nesta janela
echo [2/2] Ligando Interface (Vue.js)...
cd frontend
npm run dev