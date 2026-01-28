from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any
import pandas as pd
import traceback 
import numpy as np # Import needed to detect numpy types

router = APIRouter(prefix="/contabilidade/indicadores", tags=["Indicadores"])

# Modelo de entrada
class DadosCalculo(BaseModel):
    balanco: Dict[str, List[Dict[str, Any]]] 
    dre: Dict[str, List[Dict[str, Any]]]     

@router.post("/liquidez")
def calcular_liquidez(dados: DadosCalculo):
    print("--- INICIANDO CÁLCULO DE LIQUIDEZ ---")
    
    try:
        b = dados.balanco

        # --- FUNÇÕES AUXILIARES ---

        def somar_grupo(grupo):
            if not grupo or not isinstance(grupo, list): 
                return 0.0
            
            df = pd.DataFrame(grupo)
            
            if df.empty or 'valor' not in df.columns:
                return 0.0
            
            # .sum() returns a numpy type, so we convert to float immediately
            return float(pd.to_numeric(df['valor'], errors='coerce').fillna(0).sum())

        def achar_conta(nome_chave, balanco_dict):
            total_encontrado = 0.0
            
            for grupo_key, itens in balanco_dict.items():
                if not itens or not isinstance(itens, list):
                    continue

                df = pd.DataFrame(itens)
                
                if df.empty or 'conta' not in df.columns or 'valor' not in df.columns:
                    continue

                filtro = df['conta'].str.contains(nome_chave, case=False, na=False)
                conta_df = df[filtro]
                
                if not conta_df.empty:
                    soma_parcial = pd.to_numeric(conta_df['valor'], errors='coerce').fillna(0).sum()
                    total_encontrado += soma_parcial
            
            # Ensure return is a python float
            return float(total_encontrado)

        # --- 2. Extração dos Dados ---

        total_ac = somar_grupo(b.get('ativo_circulante', []))
        total_anc = somar_grupo(b.get('ativo_nao_circulante', []))
        total_pc = somar_grupo(b.get('passivo_circulante', []))
        total_pnc = somar_grupo(b.get('passivo_nao_circulante', []))

        disponivel = achar_conta('Caixa|Equivalentes|Disponível', b)
        estoques = achar_conta('Estoque', b)
        despesas_antecipadas = achar_conta('Despesas Antecipadas', b)
        realizavel_longo_prazo = achar_conta('Realizável a Longo Prazo', b)
        
        print(f"DEBUG VALORES: AC={total_ac}, PC={total_pc}, Disp={disponivel}, Estq={estoques}, RLP={realizavel_longo_prazo}")

        # --- 3. Cálculos dos Índices ---

        if total_pc == 0:
            return {
                "erro": "O Passivo Circulante é R$ 0,00. Divisão por zero impossível.",
                "detalhe": "Verifique se o Balanço selecionado possui valores no Passivo Circulante."
            }

        # Calculations (Results might be numpy types if operands were numpy types)
        liq_corrente = total_ac / total_pc
        liq_imediata = disponivel / total_pc
        liq_seca = (total_ac - estoques - despesas_antecipadas) / total_pc

        passivo_total = total_pc + total_pnc
        if passivo_total == 0:
            liq_geral = 0.0
        else:
            liq_geral = (total_ac + realizavel_longo_prazo) / passivo_total

        # --- 4. Retorno Formatado (CONVERTING TO PYTHON TYPES) ---
        # We use float() explicitly to ensure JSON serializability
        return {
            "indices": {
                "corrente": round(float(liq_corrente), 2),
                "imediata": round(float(liq_imediata), 2),
                "seca": round(float(liq_seca), 2),
                "geral": round(float(liq_geral), 2)
            },
            "variaveis_usadas": {
                "ativo_circulante": float(total_ac),
                "passivo_circulante": float(total_pc),
                "disponivel": float(disponivel),
                "estoques": float(estoques),
                "despesas_antecipadas": float(despesas_antecipadas),
                "realizavel_longo_prazo": float(realizavel_longo_prazo),
                "passivo_nao_circulante": float(total_pnc)
            }
        }

    except Exception as e:
        print("❌ ERRO CRÍTICO NO BACKEND:")
        traceback.print_exc() 
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno de cálculo: {str(e)}"
        )