import os
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers import investimentos

# 1. Carrega as variáveis do arquivo .env
load_dotenv()
API_TOKEN_SECRETO = os.getenv("API_TOKEN")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Depois mudaremos isso para produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Função de Segurança (O Guarda)
async def verificar_token(x_token: str = Header(...)):
    if x_token != API_TOKEN_SECRETO:
        raise HTTPException(status_code=401, detail="Token Inválido ou Ausente! 🚫")

# 3. Protegendo as Rotas
# Adicionamos 'dependencies' aqui. Agora TODAS as rotas de investimento exigem o token.
app.include_router(investimentos.router, dependencies=[Depends(verificar_token)])

@app.get("/")
def home():
    return {"status": "Sistema Online", "acesso": "Público"}