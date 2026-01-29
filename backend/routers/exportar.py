from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, List, Any
import pandas as pd
import io

router = APIRouter(prefix="/exportar", tags=["Exportação"])

# Alteramos 'dados' para Any ou Dict genérico para aceitar estruturas diferentes
class DadosExportacao(BaseModel):
    dados: Any 
    tipo: str # "balanco", "dre", "indicadores"

@router.post("/excel")
def exportar_excel(payload: DadosExportacao):
    try:
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='openpyxl')
        
        data = payload.dados
        rows = []

        # --- LÓGICA 1: BALANÇO ---
        if payload.tipo == "balanco":
            grupos_map = {
                'ativo_circulante': 'Ativo Circulante',
                'ativo_nao_circulante': 'Ativo Não Circulante',
                'passivo_circulante': 'Passivo Circulante',
                'passivo_nao_circulante': 'Passivo Não Circulante',
                'patrimonio_liquido': 'Patrimônio Líquido'
            }
            for key, label in grupos_map.items():
                items = data.get(key, [])
                if items:
                    rows.append({"Grupo": label.upper(), "Conta": "", "Valor": ""}) # Cabeçalho de Grupo
                    for item in items:
                        rows.append({
                            "Grupo": label,
                            "Conta": item.get('conta'),
                            "Valor": float(item.get('valor', 0))
                        })

        # --- LÓGICA 2: DRE ---
        elif payload.tipo == "dre":
            ordem = [
                ('receita_bruta', 'Receita Bruta'),
                ('deducoes', '(-) Deduções'),
                ('custos_producao', '(-) Custos Prod.'),
                ('custos_venda', '(-) Custos Venda'),
                ('desp_comerciais', '(-) Desp. Comerciais'),
                ('desp_administrativas', '(-) Desp. Adm'),
                ('outras_ops', '(+/-) Outras Ops'),
                ('financeiro', '(+/-) Financeiro'),
                ('impostos', '(-) Impostos')
            ]
            for key, label in ordem:
                items = data.get(key, [])
                if items:
                    rows.append({"Categoria": label.upper(), "Conta": "", "Valor": ""})
                    for item in items:
                        rows.append({
                            "Categoria": label,
                            "Conta": item.get('conta'),
                            "Valor": float(item.get('valor', 0))
                        })

        # --- LÓGICA 3: INDICADORES (A "BONITINHA") ---
        elif payload.tipo == "indicadores":
            # Helper para adicionar linha formatada
            def add_section(titulo, dados_indices, sufixo=""):
                if not dados_indices: return
                rows.append({"Categoria": titulo.upper(), "Indicador": "", "Valor": ""}) # Separador
                
                # Mapeamento de nomes amigáveis
                nomes = {
                    "corrente": "Liquidez Corrente", "seca": "Liquidez Seca", "imediata": "Liquidez Imediata", "geral": "Liquidez Geral",
                    "roi": "ROI (Retorno s/ Investimento)", "roe": "ROE (Retorno s/ PL)", "roa": "ROA (Retorno s/ Ativo)",
                    "ct_cp": "Cap. Terceiros / Cap. Próprio", "participacao_ct": "Part. Cap. Terceiros",
                    "pme": "Prazo Médio Estoques", "pmr": "Prazo Médio Recebimento", "pmp": "Prazo Médio Pagamento",
                    "ciclo_operacional": "Ciclo Operacional", "ciclo_caixa": "Ciclo de Caixa"
                }

                for chave, valor in dados_indices.items():
                    nome_bonito = nomes.get(chave, chave)
                    
                    # Formatação especial para % ou dias
                    val_fmt = valor
                    unidade = ""
                    
                    if sufixo == "%":
                        unidade = "%"
                    elif sufixo == " dias":
                        unidade = " dias"
                    elif chave in ["ct_cp"]:
                        unidade = "x" # Ex: 1.5x
                    
                    rows.append({
                        "Categoria": titulo,
                        "Indicador": nome_bonito,
                        "Valor": val_fmt,
                        "Unidade": unidade
                    })
                
                rows.append({"Categoria": "", "Indicador": "", "Valor": "", "Unidade": ""}) # Linha em branco

            # Extrai os dados agrupados
            liq = data.get('liquidez', {}).get('indices')
            rent = data.get('rentabilidade', {}).get('indices')
            endiv = data.get('endividamento', {}).get('indices')
            ativ = data.get('atividade', {}).get('indices')

            add_section("Liquidez", liq)
            add_section("Rentabilidade", rent, "%")
            add_section("Endividamento", endiv, "%") # Nota: ct_cp não é %, tratamos na lógica acima se quiser, mas genérico % funciona pra maioria
            add_section("Atividade (Ciclos)", ativ, " dias")

        # --- GERAÇÃO DO ARQUIVO ---
        df = pd.DataFrame(rows)
        
        # Nome da aba
        sheet = 'Relatório'
        df.to_excel(writer, index=False, sheet_name=sheet)
        
        # Ajuste Automático de Colunas (Beautify)
        worksheet = writer.sheets[sheet]
        for column in worksheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

        writer.close()
        output.seek(0)

        filename = f"relatorio_{payload.tipo}.xlsx"
        headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
        return StreamingResponse(output, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    except Exception as e:
        print(f"Erro exportação: {e}")
        raise HTTPException(status_code=500, detail=str(e))