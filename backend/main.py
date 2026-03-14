from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter import limiter

load_dotenv()

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
        print("Banco de dados inicializado com sucesso via create_all.")
    except Exception as e:
        print(f"Erro ao inicializar tabelas: {e}")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://adm.ceciliolab.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Adm OS Backend Online"}

from routers import auth, exportar, users, workspaces
from routers.investimentos import swing_trade, mercado
from routers.contabilidade import indicadores
from dependencies import get_current_active_user

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(workspaces.router)
app.include_router(swing_trade.router, dependencies=[Depends(get_current_active_user)])
app.include_router(indicadores.router, dependencies=[Depends(get_current_active_user)])
app.include_router(exportar.router, dependencies=[Depends(get_current_active_user)])
app.include_router(mercado.router, dependencies=[Depends(get_current_active_user)])
