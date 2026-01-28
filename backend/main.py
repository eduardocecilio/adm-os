import os
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers.investimentos import swing_trade
from routers.contabilidade import liquidez

load_dotenv()
API_TOKEN_SECRETO = os.getenv("API_TOKEN")

app = FastAPI(title="AdminOS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def verificar_token(x_token: str = Header(...)):
    if x_token != API_TOKEN_SECRETO:
        raise HTTPException(status_code=401, detail="Token Inválido! 🚫")

# --- ROTAS ---
app.include_router(swing_trade.router, dependencies=[Depends(verificar_token)])
app.include_router(liquidez.router, dependencies=[Depends(verificar_token)])

@app.get("/")
def home():
    return {
        "sistema": "AdminOS",
        "versao": "1.0.0",
        "modulos_ativos": ["Investimentos", "Contabilidade"]
    }