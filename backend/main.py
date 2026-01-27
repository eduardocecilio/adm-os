from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração para o Frontend (Vue) conseguir conversar com esse Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que qualquer origem acesse (para desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de Dados (O que o usuário precisa enviar)
class DadosOperacao(BaseModel):
    preco_compra: float
    preco_venda: float
    quantidade: int
    taxa_corretagem: float = 2.00 # Valor padrão do seu exemplo

@app.get("/")
def home():
    return {"message": "API do AdminOS está rodando! �"}

@app.post("/calcular-resultado")
def calcular_resultado(dados: DadosOperacao, tipo: str = "normal"):
    """
    tipo: 'normal' (Swing Trade) ou 'daytrade' (Day Trade)
    """
    
    # 1. Totais da Operação
    total_compra = dados.preco_compra * dados.quantidade
    total_venda = dados.preco_venda * dados.quantidade
    lucro_bruto = total_venda - total_compra

    # 2. Definição de Taxas (Baseado no seu exemplo)
    if tipo == "daytrade":
        aliquota_emolumentos = 0.000250 # 0,0250%
        aliquota_ir = 0.20              # 20%
    else: # Operação Normal (Swing Trade)
        aliquota_emolumentos = 0.000345 # 0,0345%
        aliquota_ir = 0.15              # 15%

    # 3. Cálculo de Custos
    # Emolumentos incidem sobre o volume total (Compra + Venda) financeiro movimentado
    emolumentos_compra = total_compra * aliquota_emolumentos
    emolumentos_venda = total_venda * aliquota_emolumentos
    total_emolumentos = emolumentos_compra + emolumentos_venda

    # Corretagem (Cobrada na compra E na venda)
    total_corretagem = dados.taxa_corretagem * 2

    custos_totais = total_corretagem + total_emolumentos

    # 4. Apuração Final
    lucro_antes_ir = lucro_bruto - custos_totais
    
    # IR só é cobrado se houver lucro positivo
    imposto_renda = 0.0
    if lucro_antes_ir > 0:
        imposto_renda = lucro_antes_ir * aliquota_ir

    lucro_liquido = lucro_antes_ir - imposto_renda

    # 5. Retorno Formatado (JSON)
    return {
        "resumo": {
            "tipo_operacao": "Day Trade" if tipo == "daytrade" else "Swing Trade",
            "lucro_bruto": round(lucro_bruto, 2),
            "custos_totais": round(custos_totais, 4), # 4 casas decimais como no exemplo
            "lucro_antes_ir": round(lucro_antes_ir, 4),
            "imposto_renda": round(imposto_renda, 4),
            "lucro_liquido": round(lucro_liquido, 2)
        },
        "detalhes_custos": {
            "corretagem": total_corretagem,
            "emolumentos": round(total_emolumentos, 4)
        }
    }