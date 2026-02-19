from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from routers import exportar
import os
from dotenv import load_dotenv

# --- IMPORTS DOS ROTEADORES ---
from routers.investimentos import swing_trade
from routers.contabilidade import indicadores
from routers.investimentos import mercado
from routers import auth

app = FastAPI(
    title="Adm OS",
    docs_url=None if os.getenv("ENV") == "production" else "/docs",
    redoc_url=None
)

# Adicione localhost para testes no Mac e sua URL oficial para produção
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://adm.ceciliolab.com"
]

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
api_key_header = APIKeyHeader(name="x-token", auto_error=False)

async def verificar_token(token: str = Depends(api_key_header)):
    if not token or token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou ausente"
        )

@app.get("/")
def home():
    return {"status": "Adm OS Backend Online 🚀"} # <--- MUDADO AQUI

from routers import auth, exportar, users
from routers.investimentos import swing_trade, mercado
from routers.contabilidade import indicadores

from dependencies import get_current_active_user

# ... (rest of file) ...

# --- REGISTRO DAS ROTAS ---
app.include_router(auth.router)
app.include_router(users.router) # Added users router
app.include_router(swing_trade.router, dependencies=[Depends(get_current_active_user)])

# Rota de Indicadores
app.include_router(indicadores.router, dependencies=[Depends(get_current_active_user)])

# Rota de Exportação
app.include_router(exportar.router, dependencies=[Depends(get_current_active_user)])
app.include_router(mercado.router, dependencies=[Depends(get_current_active_user)])