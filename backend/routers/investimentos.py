from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter() # Cria um "sub-aplicativo" só para investimentos

class DadosOperacao(BaseModel):
    preco_compra: float
    preco_venda: float
    quantidade: int
    taxa_corretagem: float = 2.00 

@router.post("/calcular-resultado")
def calcular_resultado(dados: DadosOperacao, tipo: str = "normal"):
    # ... (A mesma lógica de cálculo de antes) ...
    total_compra = dados.preco_compra * dados.quantidade
    total_venda = dados.preco_venda * dados.quantidade
    lucro_bruto = total_venda - total_compra

    if tipo == "daytrade":
        aliq_emolumentos = 0.000250
        aliq_ir = 0.20
    else:
        aliq_emolumentos = 0.000345
        aliq_ir = 0.15

    custos_totais = (dados.taxa_corretagem * 2) + ((total_compra + total_venda) * aliq_emolumentos)
    lucro_antes_ir = lucro_bruto - custos_totais
    
    imposto = 0.0
    if lucro_antes_ir > 0:
        imposto = lucro_antes_ir * aliq_ir

    return {
        "resumo": {
            "lucro_liquido": round(lucro_antes_ir - imposto, 2),
            "imposto_renda": round(imposto, 4),
            "custos_totais": round(custos_totais, 4),
            "lucro_bruto": round(lucro_bruto, 2)
        }
    }