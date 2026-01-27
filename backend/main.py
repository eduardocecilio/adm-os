from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importamos o novo departamento
from routers import investimentos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Avisamos o App principal que existe o departamento de investimentos
app.include_router(investimentos.router)

@app.get("/")
def home():
    return {"status": "Sistema Online", "modulos": ["Investimentos", "Contabilidade (Em breve)"]}