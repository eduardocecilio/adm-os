from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from routers import exportar
import os
from dotenv import load_dotenv
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter import limiter

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

from database import engine, Base
import models.user
import models.workspace

@app.on_event("startup")
def startup_event():
    # Garante que as tabelas essenciais existam sem depender do Alembic no primeiro boot
    try:
        Base.metadata.create_all(bind=engine)
        print("Bando de dados inicializado com sucesso via create_all.")
    except Exception as e:
        print(f"Erro ao inicializar tabelas: {e}")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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

from routers import auth, exportar, users, workspaces
from routers.investimentos import swing_trade, mercado
from routers.contabilidade import indicadores

from dependencies import get_current_active_user

# --- REGISTRO DAS ROTAS ---
app.include_router(auth.router)
app.include_router(users.router) # Added users router
app.include_router(workspaces.router) # NO dependencies injected here because the endpoints require specific workspace dependency injections like get_workspace_access. The list_my_workspaces already uses get_current_active_user directly.
app.include_router(swing_trade.router, dependencies=[Depends(get_current_active_user)])

# Rota de Indicadores
app.include_router(indicadores.router, dependencies=[Depends(get_current_active_user)])

# Rota de Exportação
app.include_router(exportar.router, dependencies=[Depends(get_current_active_user)])
app.include_router(mercado.router, dependencies=[Depends(get_current_active_user)])