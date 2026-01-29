from fastapi import APIRouter
import yfinance as yf
import pandas as pd
import requests
import urllib3

# Desabilita avisos de SSL (para o IPCA do governo)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

router = APIRouter(prefix="/investimentos/mercado", tags=["Mercado Financeiro"])

def processar_ticker_pandas(df, symbol_key):
    """ Processa dados do Yahoo Finance para Gráficos """
    try:
        if symbol_key not in df.columns.levels[0]:
            return {"valor": 0.0, "variacao": 0.0, "history": []}

        series = df[symbol_key]['Close'].ffill().bfill()
        if series.empty: 
            return {"valor": 0.0, "variacao": 0.0, "history": []}

        current = float(series.iloc[-1])
        start = float(series.iloc[0])
        variacao = ((current - start) / start) * 100 if start > 0 else 0.0

        return {
            "valor": round(current, 2),
            "variacao": round(variacao, 2),
            "history": series.fillna(0).tolist()
        }
    except:
        return {"valor": 0.0, "variacao": 0.0, "history": []}

def get_indicador_simples(tipo):
    """
    Busca apenas o valor ATUAL (sem gráfico) para evitar erros.
    """
    try:
        if tipo == "selic":
            # BrasilAPI é excelente para taxa atual
            resp = requests.get("https://brasilapi.com.br/api/taxas/v1/selic", timeout=5)
            if resp.status_code == 200:
                val = resp.json()['valor']
                return { "valor": f"{val}%", "variacao": 0, "history": [] } # History vazio = sem gráfico
        
        elif tipo == "ipca":
            # BCB apenas último valor (mais leve que baixar histórico)
            url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.13522/dados/ultimos/1?formato=json"
            resp = requests.get(url, timeout=5, verify=False) # SSL ignorado
            if resp.status_code == 200:
                val = resp.json()[0]['valor']
                return { "valor": f"{val}%", "variacao": 0, "history": [] }

    except Exception as e:
        print(f"Erro indicador {tipo}: {e}")
    
    return { "valor": "...", "variacao": 0, "history": [] }

@router.get("/resumo")
def get_resumo_mercado(periodo: str = "1mo"):
    
    # Configuração Yahoo
    p_yahoo = "1mo"
    i_yahoo = "1d"
    if periodo == "1D": p_yahoo, i_yahoo = "1d", "15m"
    elif periodo == "1A": p_yahoo, i_yahoo = "1y", "1wk"

    tickers = ["^BVSP", "BRL=X", "EURBRL=X", "BTC-USD"]

    try:
        # 1. Mercado (Com Gráficos) - Yahoo
        df = yf.download(tickers, period=p_yahoo, interval=i_yahoo, group_by='ticker', progress=False)
        
        # Sintético BTC-BRL
        if not df.empty:
            btc_usd = df['BTC-USD']['Close'].ffill().bfill()
            usd_brl = df['BRL=X']['Close'].ffill().bfill()
            df_synthetic = pd.DataFrame({'Close': btc_usd * usd_brl})
            df = pd.concat([df, pd.concat({'BTC-BRL': df_synthetic}, axis=1)], axis=1)

        # 2. Governo (Sem Gráficos, Só Valor)
        print(">>> Buscando dados Gov (Simples)...") 
        selic = get_indicador_simples("selic")
        ipca = get_indicador_simples("ipca")

        return {
            "ibov": processar_ticker_pandas(df, '^BVSP'),
            "dolar": processar_ticker_pandas(df, 'BRL=X'),
            "euro": processar_ticker_pandas(df, 'EURBRL=X'),
            "btc": {
                "usd": processar_ticker_pandas(df, 'BTC-USD'),
                "brl": processar_ticker_pandas(df, 'BTC-BRL')
            },
            "selic": selic,
            "ipca": ipca
        }

    except Exception as e:
        print(f"❌ Erro Backend: {e}")
        empty = {"valor": 0, "variacao": 0, "history": []}
        return { 
            "ibov": empty, "dolar": empty, "euro": empty, 
            "btc": {"usd": empty, "brl": empty}, 
            "selic": empty, "ipca": empty 
        }