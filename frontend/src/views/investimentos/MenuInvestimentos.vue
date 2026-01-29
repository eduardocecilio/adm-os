<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import ModuleLayout from '../../components/ModuleLayout.vue'
import { menuInvestimentos } from '../../constants/menus/menuInvestimentos.js'

const periodoGrafico = ref('1M')
const moedaBaseCripto = ref('BRL')
const loading = ref(true)
const erro = ref(null)

const dados = ref({
  ibov: { valor: 0, variacao: 0, history: [], loading: true },
  dolar: { valor: 0, variacao: 0, history: [], loading: true },
  euro: { valor: 0, variacao: 0, history: [], loading: true },
  btc: { brl: { valor: 0, variacao: 0, history: [] }, usd: { valor: 0, variacao: 0, history: [] }, loading: true },
  selic: { valor: '...', loading: true },
  ipca: { valor: '...', loading: true }
})

const carregarDadosMercado = async (periodo) => {
  // Loading visual apenas onde tem gráfico dinâmico
  dados.value.ibov.loading = true
  dados.value.dolar.loading = true
  dados.value.euro.loading = true
  dados.value.btc.loading = true
  
  try {
    const resp = await fetch(`http://127.0.0.1:8000/investimentos/mercado/resumo?periodo=${periodo}`)
    if (!resp.ok) throw new Error("Offline")
    const json = await resp.json()

    dados.value.ibov = { ...json.ibov, valor: formatInt(json.ibov.valor) + ' pts', loading: false }
    dados.value.dolar = { ...json.dolar, loading: false }
    dados.value.euro = { ...json.euro, loading: false }
    dados.value.btc = { brl: json.btc.brl, usd: json.btc.usd, loading: false }
    dados.value.selic = { ...json.selic, loading: false }
    dados.value.ipca = { ...json.ipca, loading: false }

  } catch (e) {
    erro.value = "Erro ao atualizar mercado."
  } finally {
    loading.value = false
  }
}

watch(periodoGrafico, (n) => carregarDadosMercado(n))
onMounted(() => carregarDadosMercado('1M'))

// Utils
const getSvgPath = (dataPoints, width = 120, height = 40) => {
  if (!dataPoints || dataPoints.length < 2) return ""
  const min = Math.min(...dataPoints)
  const max = Math.max(...dataPoints)
  const range = max - min || 1
  const stepX = width / (dataPoints.length - 1)
  let path = `M 0 ${height - ((dataPoints[0] - min) / range) * height}`
  dataPoints.forEach((point, i) => { if(i===0)return; path += ` L ${i*stepX} ${height - ((point - min) / range) * height}` })
  return path
}
const getChartColor = (v) => v >= 0 ? '#27ae60' : '#c0392b'
const formatCurrency = (v, c='BRL') => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: c }).format(v)
const formatInt = (v) => new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 0 }).format(v)
const formatPercent = (v) => `${v >= 0 ? '+' : ''}${parseFloat(v || 0).toFixed(2)}%`
const btcDisplay = computed(() => moedaBaseCripto.value === 'BRL' ? dados.value.btc.brl : dados.value.btc.usd)
</script>

<template>
  <ModuleLayout titulo="Investimentos" emoji="📈" :itensMenu="menuInvestimentos">
    <div class="market-dashboard">
      <header class="dash-header">
        <h2>Mesa de Operações</h2>
        <p>Visão global de Câmbio, Cripto e Indicadores.</p>
      </header>

      <div class="time-selector-container">
        <span class="label">Período:</span>
        <div class="time-selector">
          <button :class="{ active: periodoGrafico === '1D' }" @click="periodoGrafico = '1D'">1D</button>
          <button :class="{ active: periodoGrafico === '1M' }" @click="periodoGrafico = '1M'">1M</button>
          <button :class="{ active: periodoGrafico === '1A' }" @click="periodoGrafico = '1A'">1A</button>
        </div>
      </div>

      <div class="main-grid">
        <div class="column-section">
          <h3 class="sec-title">💵 Câmbio</h3>
          <div class="fiat-grid">
            <div class="card-market">
              <div class="card-top">
                <div class="info"><span class="name">🇺🇸 Dólar</span><strong v-if="!dados.dolar.loading">{{ formatCurrency(dados.dolar.valor) }}</strong><span v-else>...</span></div>
                <div class="var-badge" :class="dados.dolar.variacao >= 0 ? 'pos' : 'neg'">{{ formatPercent(dados.dolar.variacao) }}</div>
              </div>
              <div class="mini-chart"><svg width="100%" height="40" viewBox="0 0 120 40" preserveAspectRatio="none" v-if="!dados.dolar.loading"><path :d="getSvgPath(dados.dolar.history)" fill="none" :stroke="getChartColor(dados.dolar.variacao)" stroke-width="2" /></svg></div>
            </div>
            <div class="card-market">
              <div class="card-top">
                <div class="info"><span class="name">🇪🇺 Euro</span><strong v-if="!dados.euro.loading">{{ formatCurrency(dados.euro.valor) }}</strong><span v-else>...</span></div>
                <div class="var-badge" :class="dados.euro.variacao >= 0 ? 'pos' : 'neg'">{{ formatPercent(dados.euro.variacao) }}</div>
              </div>
              <div class="mini-chart"><svg width="100%" height="40" viewBox="0 0 120 40" preserveAspectRatio="none" v-if="!dados.euro.loading"><path :d="getSvgPath(dados.euro.history)" fill="none" :stroke="getChartColor(dados.euro.variacao)" stroke-width="2" /></svg></div>
            </div>
          </div>
        </div>

        <div class="column-section">
          <div class="sec-header-row">
            <h3 class="sec-title">₿ Cripto</h3>
            <div class="toggle-switch">
              <span :class="{ active: moedaBaseCripto === 'BRL' }" @click="moedaBaseCripto = 'BRL'">R$</span>
              <span :class="{ active: moedaBaseCripto === 'USD' }" @click="moedaBaseCripto = 'USD'">US$</span>
            </div>
          </div>
          <div class="card-crypto-big">
            <div class="crypto-header"><img src="https://cryptologos.cc/logos/bitcoin-btc-logo.svg?v=025" width="32"><span>Bitcoin</span></div>
            <strong class="crypto-val" v-if="!dados.btc.loading">{{ formatCurrency(btcDisplay.valor, moedaBaseCripto) }}</strong>
            <span class="crypto-loading" v-else>...</span>
            <div class="crypto-chart-area">
              <svg width="100%" height="60" viewBox="0 0 120 60" preserveAspectRatio="none" v-if="!dados.btc.loading">
                <path :d="getSvgPath(btcDisplay.history, 120, 60) + ' L 120 60 L 0 60 Z'" :fill="getChartColor(btcDisplay.variacao)" opacity="0.1" />
                <path :d="getSvgPath(btcDisplay.history, 120, 60)" fill="none" :stroke="getChartColor(btcDisplay.variacao)" stroke-width="2.5" />
              </svg>
            </div>
            <div class="crypto-footer"><small>Variação:</small><span :class="btcDisplay.variacao >= 0 ? 'text-pos' : 'text-neg'">{{ formatPercent(btcDisplay.variacao) }}</span></div>
          </div>
        </div>
      </div>

      <section class="indices-section">
        <h3 class="sec-title">📊 Índices Macroeconômicos</h3>
        <div class="indices-grid">
          
          <div class="card-indice">
            <div class="idx-header"><span class="idx-name">Ibovespa</span><strong v-if="!dados.ibov.loading">{{ dados.ibov.valor }}</strong><span v-else>...</span></div>
            <div class="mini-chart"><svg width="100%" height="40" viewBox="0 0 120 40" preserveAspectRatio="none" v-if="!dados.ibov.loading"><path :d="getSvgPath(dados.ibov.history)" fill="none" :stroke="getChartColor(dados.ibov.variacao)" stroke-width="2" /></svg></div>
            <span class="idx-var" :class="dados.ibov.variacao >= 0 ? 'text-pos' : 'text-neg'">{{ formatPercent(dados.ibov.variacao) }}</span>
          </div>

          <div class="card-indice simple">
            <div class="icon-bg">🇧🇷</div>
            <span class="idx-name">Taxa Selic</span>
            <strong class="idx-val big">{{ dados.selic.valor }}</strong>
            <small class="text-neutral">Meta Anual (BrasilAPI)</small>
          </div>

          <div class="card-indice simple">
            <div class="icon-bg">🛒</div>
            <span class="idx-name">IPCA (12m)</span>
            <strong class="idx-val big">{{ dados.ipca.valor }}</strong>
            <small class="text-neutral">Inflação Acumulada (BCB)</small>
          </div>

        </div>
      </section>

    </div>
  </ModuleLayout>
</template>

<style scoped>
/* Mesmos estilos de antes, apenas ajustes finos para os cards simples */
.market-dashboard { max-width: 1000px; margin: 0 auto; padding: 20px 0; }
.dash-header { text-align: center; margin-bottom: 30px; }
.dash-header h2 { color: #2c3e50; font-size: 1.8rem; margin: 0; }
.dash-header p { color: #7f8c8d; margin-top: 5px; }

.time-selector-container { display: flex; justify-content: flex-end; align-items: center; gap: 10px; margin-bottom: 20px; }
.time-selector-container .label { font-size: 0.85rem; color: #7f8c8d; }
.time-selector { display: flex; background: #fff; border: 1px solid #e0e0e0; border-radius: 6px; overflow: hidden; }
.time-selector button { border: none; background: none; padding: 6px 12px; cursor: pointer; font-size: 0.8rem; color: #7f8c8d; border-right: 1px solid #e0e0e0; transition: 0.2s; }
.time-selector button.active { background: #2c3e50; color: white; }

.sec-title { font-size: 0.9rem; color: #95a5a6; text-transform: uppercase; font-weight: 700; margin-bottom: 15px; display: block; }
.main-grid { display: grid; grid-template-columns: 1fr 1.2fr; gap: 30px; margin-bottom: 40px; }
.fiat-grid { display: flex; flex-direction: column; gap: 15px; }

.card-market { background: white; border-radius: 10px; padding: 15px; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }
.card-market .name { font-size: 0.85rem; color: #7f8c8d; display: block; margin-bottom: 2px; }
.card-market strong { font-size: 1.3rem; color: #2c3e50; }
.var-badge { font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; font-weight: bold; }
.var-badge.pos { background: #e8f5e9; color: #27ae60; }
.var-badge.neg { background: #ffebee; color: #c0392b; }

.sec-header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.toggle-switch { background: #e0e0e0; border-radius: 20px; padding: 2px; display: flex; }
.toggle-switch span { padding: 4px 10px; border-radius: 16px; font-size: 0.75rem; font-weight: bold; cursor: pointer; color: #666; }
.toggle-switch span.active { background: white; color: #f7931a; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }

.card-crypto-big { background: linear-gradient(145deg, #1a252f 0%, #2c3e50 100%); color: white; border-radius: 12px; padding: 25px; box-shadow: 0 10px 20px rgba(44, 62, 80, 0.2); }
.crypto-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; font-weight: 600; opacity: 0.9; }
.crypto-val { font-size: 2rem; display: block; margin-bottom: 10px; }
.crypto-chart-area { height: 60px; margin-bottom: 15px; }
.crypto-footer { display: flex; justify-content: space-between; font-size: 0.85rem; opacity: 0.8; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px; }

.indices-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.card-indice { background: white; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; text-align: center; position: relative; overflow: hidden; }
.card-indice.simple { display: flex; flex-direction: column; justify-content: center; align-items: center; }
.idx-name { display: block; font-size: 0.85rem; color: #95a5a6; text-transform: uppercase; font-weight: 600; margin-bottom: 5px; }
.idx-val, .card-indice strong { font-size: 1.4rem; color: #2c3e50; display: block; }
.idx-val.big { font-size: 1.8rem; font-weight: 800; color: #2c3e50; margin: 10px 0; }
.idx-var { font-size: 0.85rem; font-weight: bold; margin-top: 5px; display: block; }

.icon-bg { font-size: 3rem; position: absolute; opacity: 0.05; top: 10px; right: 10px; pointer-events: none; }

.mini-chart { height: 40px; margin: 5px 0; }
.text-pos { color: #2ecc71; }
.text-neg { color: #e74c3c; }
.text-neutral { color: #bdc3c7; }

@media (max-width: 768px) { .main-grid, .indices-grid { grid-template-columns: 1fr; } }
</style>