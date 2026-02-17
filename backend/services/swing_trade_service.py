from pydantic import BaseModel
from config import settings

class DadosOperacao(BaseModel):
    preco_compra: float
    preco_venda: float
    quantidade: int
    taxa_corretagem: float = 2.00 

def calcular_swing_trade(dados: DadosOperacao) -> dict:
    total_compra = dados.preco_compra * dados.quantidade
    total_venda = dados.preco_venda * dados.quantidade
    lucro_bruto = total_venda - total_compra

    custos_totais = (dados.taxa_corretagem * 2) + ((total_compra + total_venda) * settings.ALIQ_EMOLUMENTOS)
    lucro_antes_ir = lucro_bruto - custos_totais
    
    imposto = 0.0
    if lucro_antes_ir > 0:
        imposto = lucro_antes_ir * settings.ALIQ_IR_SWING_TRADE

    return {
        "resumo": {
            "lucro_liquido": round(lucro_antes_ir - imposto, 2),
            "imposto_renda": round(imposto, 4),
            "custos_totais": round(custos_totais, 4),
            "lucro_bruto": round(lucro_bruto, 2)
        }
    }
