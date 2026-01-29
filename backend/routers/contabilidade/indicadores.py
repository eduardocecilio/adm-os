from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any
import pandas as pd
import traceback 
import numpy as np 
import json

router = APIRouter(prefix="/contabilidade/indicadores", tags=["Indicadores"])

# Modelo de entrada
class DadosCalculo(BaseModel):
    balanco: Dict[str, List[Dict[str, Any]]] 
    dre: Dict[str, List[Dict[str, Any]]]     

# --- FUNÇÕES AUXILIARES GERAIS ---
def to_float(valor):
    try:
        return float(valor)
    except:
        return 0.0

def somar_grupo(grupo):
    if not grupo or not isinstance(grupo, list): 
        return 0.0
    
    df = pd.DataFrame(grupo)
    if df.empty or 'valor' not in df.columns:
        return 0.0
    
    return to_float(pd.to_numeric(df['valor'], errors='coerce').fillna(0).sum())

def achar_conta_em_lista(lista_itens, termo_busca, nome_grupo="grupo"):
    if not lista_itens or not isinstance(lista_itens, list):
        return 0.0
        
    df = pd.DataFrame(lista_itens)
    if df.empty or 'conta' not in df.columns:
        return 0.0
        
    # Busca por texto (case insensitive)
    filtro = df['conta'].str.contains(termo_busca, case=False, na=False)
    conta_df = df[filtro]
    
    if not conta_df.empty:
        soma = pd.to_numeric(conta_df['valor'], errors='coerce').fillna(0).sum()
        # Debug para confirmar onde achou
        print(f"   -> [{nome_grupo}] Encontrado '{termo_busca}': R$ {soma}")
        return to_float(soma)
    return 0.0

def achar_conta_global(nome_chave, balanco_dict):
    total = 0.0
    for key, itens in balanco_dict.items():
        total += achar_conta_em_lista(itens, nome_chave, key)
    return total

# --- 1. ROTA DE LIQUIDEZ ---
@router.post("/liquidez")
def calcular_liquidez(dados: DadosCalculo):
    print("\n💧 --- CÁLCULO DE LIQUIDEZ SOLICITADO ---")
    try:
        b = dados.balanco
        
        # Totais
        total_ac = somar_grupo(b.get('ativo_circulante', []))
        total_pc = somar_grupo(b.get('passivo_circulante', []))
        total_pnc = somar_grupo(b.get('passivo_nao_circulante', []))

        # Contas Específicas
        print("🔍 Buscando contas específicas para Liquidez:")
        disponivel = achar_conta_global('Caixa|Equivalentes|Disponível', b)
        estoques = achar_conta_global('Estoque', b)
        despesas_antecipadas = achar_conta_global('Despesas Antecipadas', b)
        realizavel_longo_prazo = achar_conta_global('Realizável a Longo Prazo', b)
        
        if total_pc == 0:
            return {"erro": "Passivo Circulante é zero."}

        passivo_total = total_pc + total_pnc
        liq_geral = (total_ac + realizavel_longo_prazo) / passivo_total if passivo_total > 0 else 0.0

        return {
            "indices": {
                "corrente": round(total_ac / total_pc, 2),
                "imediata": round(disponivel / total_pc, 2),
                "seca": round((total_ac - estoques - despesas_antecipadas) / total_pc, 2),
                "geral": round(liq_geral, 2)
            },
            "variaveis_usadas": {
                "ativo_circulante": total_ac,
                "passivo_circulante": total_pc,
                "disponivel": disponivel,
                "estoques": estoques,
                "passivo_nao_circulante": total_pnc
            }
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# --- 2. ROTA DE RENTABILIDADE ---
@router.post("/rentabilidade")
def calcular_rentabilidade(dados: DadosCalculo):
    print("\n📈 --- CÁLCULO DE RENTABILIDADE SOLICITADO ---")
    try:
        b = dados.balanco
        d = dados.dre

        # DRE
        rec_bruta = somar_grupo(d.get('receita_bruta', []))
        deducoes = somar_grupo(d.get('deducoes', []))
        rec_liquida = rec_bruta - deducoes

        total_custos = (
            somar_grupo(d.get('custos', [])) + 
            somar_grupo(d.get('custos_producao', [])) + 
            somar_grupo(d.get('custos_venda', []))
        )
        lucro_bruto = rec_liquida - total_custos

        total_despesas = (
            somar_grupo(d.get('despesas', [])) +
            somar_grupo(d.get('desp_comerciais', [])) +
            somar_grupo(d.get('desp_administrativas', []))
        )
        outras_ops = somar_grupo(d.get('outras_ops', [])) 
        outras_receitas = somar_grupo(d.get('outras_receitas', []))

        lucro_operacional = lucro_bruto - total_despesas + outras_ops + outras_receitas

        financeiro = somar_grupo(d.get('financeiro', [])) + somar_grupo(d.get('resultado_financeiro', []))
        lair = lucro_operacional + financeiro
        
        impostos = somar_grupo(d.get('impostos', [])) + somar_grupo(d.get('impostos_lucro', []))
        lucro_liquido = lair - impostos

        # BALANÇO
        ativo_total = somar_grupo(b.get('ativo_circulante', [])) + somar_grupo(b.get('ativo_nao_circulante', []))
        patrimonio_liquido = somar_grupo(b.get('patrimonio_liquido', []))

        # Investimento (ROI)
        emprestimos_cp = achar_conta_global('Empréstimos|Financiamentos', {'pc': b.get('passivo_circulante', [])})
        emprestimos_lp = achar_conta_global('Empréstimos|Financiamentos', {'pnc': b.get('passivo_nao_circulante', [])})
        investimento_total = emprestimos_cp + emprestimos_lp + patrimonio_liquido

        # ÍNDICES (Baseados no Lucro Líquido)
        roa = (lucro_liquido / ativo_total * 100) if ativo_total > 0 else 0.0
        roi = (lucro_liquido / investimento_total * 100) if investimento_total > 0 else 0.0
        roe = (lucro_liquido / patrimonio_liquido * 100) if patrimonio_liquido > 0 else 0.0

        return {
            "indices": {
                "roa": round(to_float(roa), 2),
                "roi": round(to_float(roi), 2),
                "roe": round(to_float(roe), 2)
            },
            "variaveis_usadas": {
                "lucro_operacional": to_float(lucro_operacional),
                "lucro_liquido": to_float(lucro_liquido),
                "ativo_total": to_float(ativo_total),
                "patrimonio_liquido": to_float(patrimonio_liquido),
                "investimento_total": to_float(investimento_total)
            }
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# --- 3. ROTA DE ENDIVIDAMENTO ---
@router.post("/endividamento")
def calcular_endividamento(dados: DadosCalculo):
    print("\n⚖️ --- CÁLCULO DE ENDIVIDAMENTO SOLICITADO ---")
    try:
        b = dados.balanco
        total_pc = somar_grupo(b.get('passivo_circulante', []))
        total_pnc = somar_grupo(b.get('passivo_nao_circulante', []))
        total_pl = somar_grupo(b.get('patrimonio_liquido', []))

        cap_terceiros = total_pc + total_pnc
        passivo_total_geral = cap_terceiros + total_pl

        indice_ct_cp = (cap_terceiros / total_pl) if total_pl > 0 else 0.0
        participacao_ct = (cap_terceiros / passivo_total_geral * 100) if passivo_total_geral > 0 else 0.0

        return {
            "indices": {
                "ct_cp": round(to_float(indice_ct_cp), 2),
                "participacao_ct": round(to_float(participacao_ct), 2)
            },
            "variaveis_usadas": {
                "cap_terceiros": to_float(cap_terceiros),
                "patrimonio_liquido": to_float(total_pl),
                "passivo_total": to_float(passivo_total_geral)
            }
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# --- 4. ROTA DE ATIVIDADE (CICLOS) ---
@router.post("/atividade")
def calcular_atividade(dados: DadosCalculo):
    print("\n🔄 --- CÁLCULO DE ATIVIDADE (CICLOS) SOLICITADO ---")
    try:
        b = dados.balanco
        d = dados.dre

        # 1. Balanço
        estoque_atual = achar_conta_global('Estoque', b)
        fornecedores_atual = achar_conta_global('Fornecedores', b)
        contas_receber_atual = achar_conta_global('Contas a Receber|Clientes', b)

        # 2. DRE
        receita_bruta = somar_grupo(d.get('receita_bruta', []))
        
        # CMV (Custos Venda + Custos Gerais)
        cmv = somar_grupo(d.get('custos_venda', [])) + somar_grupo(d.get('custos', []))

        # Serviços de Terceiros (COMPOSIÇÃO DAS COMPRAS)
        print("🔎 Compondo Compras Anuais:")
        servicos_cto = achar_conta_em_lista(d.get('custos_producao', []), 'Serviços de Terceiros', 'custos_producao')
        servicos_cml = achar_conta_em_lista(d.get('desp_comerciais', []), 'Serviços de Terceiros', 'desp_comerciais')
        servicos_adm = achar_conta_em_lista(d.get('desp_administrativas', []), 'Serviços de Terceiros', 'desp_administrativas')

        # Compras Anuais = CMV + Serviços (CTO + CML + ADM)
        compras_anuais = cmv + servicos_cto + servicos_cml + servicos_adm

        print(f"📊 DEBUG COMPRAS: CMV={cmv} + CTO={servicos_cto} + CML={servicos_cml} + ADM={servicos_adm}")
        print(f"   = Total Compras: {compras_anuais}")
        print(f"   = Fornecedores Balanço: {fornecedores_atual}")

        # 3. Cálculos
        # PME
        pme = (estoque_atual / cmv * 360) if cmv > 0 else 0.0

        # PMR
        pmr = (contas_receber_atual / receita_bruta * 360) if receita_bruta > 0 else 0.0

        # PMP
        pmp = (fornecedores_atual / compras_anuais * 360) if compras_anuais > 0 else 0.0

        # Ciclos
        ciclo_operacional = pme + pmr
        ciclo_caixa = ciclo_operacional - pmp

        return {
            "indices": {
                "pme": round(to_float(pme), 0),
                "pmr": round(to_float(pmr), 0),
                "pmp": round(to_float(pmp), 0),
                "ciclo_operacional": round(to_float(ciclo_operacional), 0),
                "ciclo_caixa": round(to_float(ciclo_caixa), 0)
            },
            "variaveis_usadas": {
                "estoque": to_float(estoque_atual),
                "contas_receber": to_float(contas_receber_atual),
                "fornecedores": to_float(fornecedores_atual),
                "receita_bruta": to_float(receita_bruta),
                "cmv": to_float(cmv),
                "compras_anuais": to_float(compras_anuais)
            }
        }
    except Exception as e:
        print("❌ ERRO ATIVIDADE:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))