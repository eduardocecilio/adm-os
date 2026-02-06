@echo off
TITLE AdmOS Launcher

:: Esta linha garante que o script saiba onde está a pasta raiz, independente de onde foi chamado
set ROOT_DIR=%~dp0..
cd /d "%ROOT_DIR%"

echo ==================================================
echo * INICIANDO ADM OS (MODO WINDOWS)
echo ==================================================
echo Local: %CD%
echo.

:: Verifica se a venv existe na pasta correta
if not exist "backend\venv" (
    echo [ERRO] A pasta 'venv' nao foi encontrada em: %CD%\backend\venv
    echo [DICA] Rode: python -m venv backend\venv
    pause
    exit
)

echo [1/2] Ligando API (Python/FastAPI)...
start "AdmOS - Backend API" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload --port 8001"

echo [2/2] Ligando Interface (Vue.js)...
cd frontend
npm run dev