from fastapi import APIRouter
from services.swing_trade_service import calcular_swing_trade, DadosOperacao

# Criamos o router específico desta operação
router = APIRouter(prefix="/investimentos/swing-trade", tags=["Investimentos"])

@router.post("/calcular")
def calcular_resultado(dados: DadosOperacao):
    return calcular_swing_trade(dados)