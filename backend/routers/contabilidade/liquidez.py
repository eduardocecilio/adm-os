from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/contabilidade/liquidez", tags=["Contabilidade"])

class DadosBalanco(BaseModel):
    ativo_circulante: float
    passivo_circulante: float
    estoques: float = 0.0

@router.post("/calcular")
def calcular_liquidez(dados: DadosBalanco):
    # Evitar divisão por zero
    if dados.passivo_circulante == 0:
        return {"erro": "Passivo Circulante não pode ser zero."}

    # 1. Liquidez Corrente (Capacidade de curto prazo)
    liquidez_corrente = dados.ativo_circulante / dados.passivo_circulante

    # 2. Liquidez Seca (Sem depender de vender estoque)
    liquidez_seca = (dados.ativo_circulante - dados.estoques) / dados.passivo_circulante

    # Análise automática (Inteligência do Sistema)
    analise = "Saudável"
    if liquidez_corrente < 1:
        analise = "Crítica (Não paga as dívidas de curto prazo)"
    elif liquidez_corrente < 1.5:
        analise = "Alerta (Margem apertada)"

    return {
        "indicadores": {
            "liquidez_corrente": round(liquidez_corrente, 2),
            "liquidez_seca": round(liquidez_seca, 2)
        },
        "analise_ia": analise
    }