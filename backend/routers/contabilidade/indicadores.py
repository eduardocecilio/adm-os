from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import pandas as pd
import traceback 
import numpy as np 
import json

router = APIRouter(prefix="/contabilidade/indicadores", tags=["Indicadores"])

# Atualizamos o modelo para aceitar o Balanço Anterior (Opcional)
class DadosCalculo(BaseModel):
    balanco: Dict[str, List[Dict[str, Any]]] 
    dre: Dict[str, List[Dict[str, Any]]]
    balanco_anterior: Optional[Dict[str, List[Dict[str, Any]]]] = None # <--- NOVO

# --- FUNÇÕES AUXILIARES ---
def to_float(valor):
    try:
        return float(valor)
    except:
        return 0.0

def somar_grupo(grupo):
    if not grupo or not isinstance(grupo, list): return 0.0
    df = pd.DataFrame(grupo)
    if df.empty or 'valor' not in df.columns: return 0.0
    return to_float(pd.to_numeric(df['valor'], errors='coerce').fillna(0).sum())

def achar_conta_em_lista(lista_itens, termo_busca, nome_grupo="grupo"):
    if not lista_itens or not isinstance(lista_itens, list): return 0.0
    df = pd.DataFrame(lista_itens)
    if df.empty or 'conta' not in df.columns: return 0.0
    filtro = df['conta'].str.contains(termo_busca, case=False, na=False)
    conta_df = df[filtro]
    if not conta_df.empty:
        soma = pd.to_numeric(conta_df['valor'], errors='coerce').fillna(0).sum()
        return to_float(soma)
    return 0.0

def achar_conta_global(nome_chave, balanco_dict):
    if not balanco_dict: return 0.0
    total = 0.0
    for key, itens in balanco_dict.items():
        total += achar_conta_em_lista(itens, nome_chave, key)
    return total

# --- NOVA FUNÇÃO INTELIGENTE DE MÉDIA ---
def get_medio(valor_atual, balanco_anterior_dict, termo_busca_global=None, grupo_especifico=None):
    """
    Se existir balanço anterior, calcula (Atual + Anterior) / 2.
    Se não, retorna apenas o Atual.
    """
    if balanco_anterior_dict is None:
        return valor_atual
    
    valor_anterior = 0.0
    
    # Se for busca por termo (ex: "Estoque")
    if termo_busca_global:
        valor_anterior = achar_conta_global(termo_busca_global, balanco_anterior_dict)
    
    # Se for busca por grupo inteiro (ex: Patrimonio Liquido)
    elif grupo_especifico:
        valor_anterior = somar_grupo(balanco_anterior_dict.get(grupo_especifico, []))
    
    return (valor_atual + valor_anterior) / 2

# --- ROTA DE LIQUIDEZ (Não usa média, usa foto do momento) ---
@router.post("/liquidez")
def calcular_liquidez(dados: DadosCalculo):
    # ... (MANTENHA O CÓDIGO DA LIQUIDEZ IGUAL AO ANTERIOR) ...
    # Liquidez é capacidade de pagamento IMEDIATA, então usa o saldo atual, não médio.
    try:
        b = dados.balanco
        total_ac = somar_grupo(b.get('ativo_circulante', []))
        total_pc = somar_grupo(b.get('passivo_circulante', []))
        total_pnc = somar_grupo(b.get('passivo_nao_circulante', []))
        disponivel = achar_conta_global('Caixa|Equivalentes|Disponível', b)
        estoques = achar_conta_global('Estoque', b)
        despesas_antecipadas = achar_conta_global('Despesas Antecipadas', b)
        realizavel_longo_prazo = achar_conta_global('Realizável a Longo Prazo', b)
        
        passivo_total = total_pc + total_pnc
        liq_geral = (total_ac + realizavel_longo_prazo) / passivo_total if passivo_total > 0 else 0.0

        return {
            "indices": {
                "corrente": round(total_ac / total_pc, 2) if total_pc else 0,
                "imediata": round(disponivel / total_pc, 2) if total_pc else 0,
                "seca": round((total_ac - estoques - despesas_antecipadas) / total_pc, 2) if total_pc else 0,
                "geral": round(liq_geral, 2)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ROTA DE RENTABILIDADE (USA MÉDIA) ---
@router.post("/rentabilidade")
def calcular_rentabilidade(dados: DadosCalculo):
    print("\n📈 --- CÁLCULO DE RENTABILIDADE (COM MÉDIA) ---")
    try:
        b = dados.balanco
        b_ant = dados.balanco_anterior # Pode ser None
        d = dados.dre

        # DRE (Fluxo do período, não faz média)
        rec_bruta = somar_grupo(d.get('receita_bruta', []))
        deducoes = somar_grupo(d.get('deducoes', []))
        rec_liquida = rec_bruta - deducoes
        
        total_custos = somar_grupo(d.get('custos', [])) + somar_grupo(d.get('custos_producao', [])) + somar_grupo(d.get('custos_venda', []))
        lucro_bruto = rec_liquida - total_custos
        
        total_despesas = somar_grupo(d.get('despesas', [])) + somar_grupo(d.get('desp_comerciais', [])) + somar_grupo(d.get('desp_administrativas', []))
        outras = somar_grupo(d.get('outras_ops', [])) + somar_grupo(d.get('outras_receitas', []))
        lucro_operacional = lucro_bruto - total_despesas + outras
        
        financeiro = somar_grupo(d.get('financeiro', [])) + somar_grupo(d.get('resultado_financeiro', []))
        impostos = somar_grupo(d.get('impostos', [])) + somar_grupo(d.get('impostos_lucro', []))
        lucro_liquido = lucro_operacional + financeiro - impostos

        # BALANÇO (Aqui aplicamos a média)
        
        # 1. Ativo Total Médio
        ativo_total_atual = somar_grupo(b.get('ativo_circulante', [])) + somar_grupo(b.get('ativo_nao_circulante', []))
        ativo_total_medio = get_medio(ativo_total_atual, b_ant, grupo_especifico=None) 
        # Nota: para ativo total teríamos que somar os grupos do anterior, mas para simplificar, 
        # vamos assumir que se b_ant existe, calculamos a soma dele na hora:
        if b_ant:
            ativo_total_ant = somar_grupo(b_ant.get('ativo_circulante', [])) + somar_grupo(b_ant.get('ativo_nao_circulante', []))
            ativo_total_medio = (ativo_total_atual + ativo_total_ant) / 2

        # 2. PL Médio
        pl_atual = somar_grupo(b.get('patrimonio_liquido', []))
        pl_medio = get_medio(pl_atual, b_ant, grupo_especifico='patrimonio_liquido')

        # 3. Investimento Médio (Emp CP + Emp LP + PL)
        emp_cp_atual = achar_conta_global('Empréstimos|Financiamentos', {'pc': b.get('passivo_circulante', [])})
        emp_lp_atual = achar_conta_global('Empréstimos|Financiamentos', {'pnc': b.get('passivo_nao_circulante', [])})
        investimento_atual = emp_cp_atual + emp_lp_atual + pl_atual
        
        investimento_medio = investimento_atual
        if b_ant:
            emp_cp_ant = achar_conta_global('Empréstimos|Financiamentos', {'pc': b_ant.get('passivo_circulante', [])})
            emp_lp_ant = achar_conta_global('Empréstimos|Financiamentos', {'pnc': b_ant.get('passivo_nao_circulante', [])})
            pl_ant = somar_grupo(b_ant.get('patrimonio_liquido', []))
            investimento_ant = emp_cp_ant + emp_lp_ant + pl_ant
            investimento_medio = (investimento_atual + investimento_ant) / 2

        # CÁLCULOS
        roa = (lucro_liquido / ativo_total_medio * 100) if ativo_total_medio > 0 else 0.0
        roi = (lucro_liquido / investimento_medio * 100) if investimento_medio > 0 else 0.0
        roe = (lucro_liquido / pl_medio * 100) if pl_medio > 0 else 0.0

        return {
            "indices": { "roa": round(roa, 2), "roi": round(roi, 2), "roe": round(roe, 2) },
            "meta_dados": { "usou_media": bool(b_ant is not None) }
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# --- ROTA DE ENDIVIDAMENTO (Não usa média) ---
@router.post("/endividamento")
def calcular_endividamento(dados: DadosCalculo):
    # Endividamento é foto estrutural, usa o atual
    try:
        b = dados.balanco
        total_pc = somar_grupo(b.get('passivo_circulante', []))
        total_pnc = somar_grupo(b.get('passivo_nao_circulante', []))
        total_pl = somar_grupo(b.get('patrimonio_liquido', []))

        cap_terceiros = total_pc + total_pnc
        passivo_total = cap_terceiros + total_pl

        indice_ct_cp = (cap_terceiros / total_pl) if total_pl > 0 else 0.0
        participacao_ct = (cap_terceiros / passivo_total * 100) if passivo_total > 0 else 0.0

        return {
            "indices": { "ct_cp": round(indice_ct_cp, 2), "participacao_ct": round(participacao_ct, 2) }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ROTA DE ATIVIDADE (USA MÉDIA) ---
@router.post("/atividade")
def calcular_atividade(dados: DadosCalculo):
    print("\n🔄 --- CÁLCULO DE ATIVIDADE (COM MÉDIA) ---")
    try:
        b = dados.balanco
        b_ant = dados.balanco_anterior
        d = dados.dre

        # DRE
        receita_bruta = somar_grupo(d.get('receita_bruta', []))
        cmv = somar_grupo(d.get('custos_venda', [])) + somar_grupo(d.get('custos', []))
        
        # Compras
        servicos_cto = achar_conta_em_lista(d.get('custos_producao', []), 'Serviços de Terceiros')
        servicos_cml = achar_conta_em_lista(d.get('desp_comerciais', []), 'Serviços de Terceiros')
        servicos_adm = achar_conta_em_lista(d.get('desp_administrativas', []), 'Serviços de Terceiros')
        compras_anuais = cmv + servicos_cto + servicos_cml + servicos_adm

        # BALANÇO (Médias)
        estoque_atual = achar_conta_global('Estoque', b)
        estoque_medio = get_medio(estoque_atual, b_ant, termo_busca_global='Estoque')

        receber_atual = achar_conta_global('Contas a Receber|Clientes', b)
        receber_medio = get_medio(receber_atual, b_ant, termo_busca_global='Contas a Receber|Clientes')

        forn_atual = achar_conta_global('Fornecedores', b)
        forn_medio = get_medio(forn_atual, b_ant, termo_busca_global='Fornecedores')

        print(f"📊 DEBUG ATIVIDADE: Est.Médio={estoque_medio}, Forn.Médio={forn_medio}")

        # Cálculos
        pme = (estoque_medio / cmv * 360) if cmv > 0 else 0.0
        pmr = (receber_medio / receita_bruta * 360) if receita_bruta > 0 else 0.0
        pmp = (forn_medio / compras_anuais * 360) if compras_anuais > 0 else 0.0

        return {
            "indices": {
                "pme": round(pme, 0), "pmr": round(pmr, 0), "pmp": round(pmp, 0),
                "ciclo_operacional": round(pme + pmr, 0),
                "ciclo_caixa": round((pme + pmr) - pmp, 0)
            },
            "meta_dados": { "usou_media": bool(b_ant is not None) }
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))