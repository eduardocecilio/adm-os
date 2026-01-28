from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader

# --- IMPORTS DOS ROTEADORES ---
from routers.investimentos import swing_trade
# from routers.contabilidade import dre  <-- REMOVA OU COMENTE ESSA LINHA (Causa do erro)
from routers.contabilidade import indicadores # <--- MANTENHA ESSA

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Segurança
API_TOKEN = "admin-os-segredo-2026"
api_key_header = APIKeyHeader(name="x-token", auto_error=False)

async def verificar_token(token: str = Depends(api_key_header)):
    if token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou ausente"
        )

@app.get("/")
def home():
    return {"status": "AdminOS Backend Online 🚀"}

# --- REGISTRO DAS ROTAS ---
app.include_router(swing_trade.router, dependencies=[Depends(verificar_token)])
# app.include_router(dre.router, dependencies=[Depends(verificar_token)]) <-- REMOVA OU COMENTE ESTA LINHA

# Rota de Indicadores (Essa é a que queremos agora)
app.include_router(indicadores.router, dependencies=[Depends(verificar_token)])