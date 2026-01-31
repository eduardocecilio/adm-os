#!/bin/bash

# Garante que o script rode a partir da raiz do projeto, não importa de onde você chamou
cd "$(dirname "$0")/.."

echo "=================================================="
echo "🚀 INICIANDO ADMIN OS (MODO LINUX/MAC)"
echo "=================================================="

if [ ! -d "backend/venv" ]; then
    echo "[ERRO] A pasta 'venv' nao foi encontrada."
    exit 1
fi

echo "[1/2] Ligando API..."
source backend/venv/bin/activate
cd backend
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

echo "[2/2] Ligando Interface..."
cd frontend
npm run dev

kill $BACKEND_PID