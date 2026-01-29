<script setup>
import { ref, onMounted, computed } from 'vue'
import ModuleLayout from '../../components/ModuleLayout.vue'
import BtnExcel from '../../components/BtnExcel.vue'
import { menuContabilidade } from '../../constants/menus/menuContabilidade.js'

const historicoBalanco = ref([])
const historicoDRE = ref([])

const selecionadoBalanco = ref('') 
const selecionadoBalancoAnt = ref('') 
const selecionadoDRE = ref('')     

const resLiquidez = ref(null)
const resRentabilidade = ref(null)
const resEndividamento = ref(null)
const resAtividade = ref(null)

const loading = ref(false)
const erro = ref(null)

onMounted(() => {
  const savedBalanco = localStorage.getItem('historico_balanco')
  const savedDRE = localStorage.getItem('historico_dre')
  if (savedBalanco) historicoBalanco.value = JSON.parse(savedBalanco)
  if (savedDRE) historicoDRE.value = JSON.parse(savedDRE)
})

const calcularIndices = async () => {
  erro.value = null
  resLiquidez.value = null
  resRentabilidade.value = null
  resEndividamento.value = null
  resAtividade.value = null

  if (selecionadoBalanco.value === '' || selecionadoDRE.value === '') {
    erro.value = "⚠️ Por favor, selecione os dados do Período Atual (Balanço e DRE)."
    return
  }

  const balancoObj = historicoBalanco.value[selecionadoBalanco.value].dados
  const dreObj = historicoDRE.value[selecionadoDRE.value].dados
  
  let balancoAntObj = null
  if (selecionadoBalancoAnt.value !== '' && selecionadoBalancoAnt.value !== selecionadoBalanco.value) {
    balancoAntObj = historicoBalanco.value[selecionadoBalancoAnt.value].dados
  }

  const payload = { 
    balanco: balancoObj, 
    dre: dreObj,
    balanco_anterior: balancoAntObj
  }

  loading.value = true

  try {
    const headers = { 'Content-Type': 'application/json', 'x-token': 'admin-os-segredo-2026' }
    const body = JSON.stringify(payload)

    const [respLiq, respRent, respEnd, respAtiv] = await Promise.all([
      fetch('http://127.0.0.1:8000/contabilidade/indicadores/liquidez', { method: 'POST', headers, body }),
      fetch('http://127.0.0.1:8000/contabilidade/indicadores/rentabilidade', { method: 'POST', headers, body }),
      fetch('http://127.0.0.1:8000/contabilidade/indicadores/endividamento', { method: 'POST', headers, body }),
      fetch('http://127.0.0.1:8000/contabilidade/indicadores/atividade', { method: 'POST', headers, body })
    ])

    if (!respLiq.ok) throw new Error("Erro de comunicação com o servidor.")

    resLiquidez.value = await respLiq.json()
    resRentabilidade.value = await respRent.json()
    resEndividamento.value = await respEnd.json()
    resAtividade.value = await respAtiv.json()

  } catch (e) {
    erro.value = "Erro: " + e.message
  } finally {
    loading.value = false
  }
}

// Helpers Visuais
const getClassLiq = (v) => v > 1.0 ? 'text-green' : (v >= 0.9 ? 'text-orange' : 'text-red')
const getClassRent = (v) => v > 15.0 ? 'text-green' : (v > 5.0 ? 'text-orange' : 'text-red')
const getClassEndiv = (v) => v < 50.0 ? 'text-green' : (v < 70.0 ? 'text-orange' : 'text-red')
const getClassCiclo = (v) => v < 60 ? 'text-green' : (v < 90 ? 'text-orange' : 'text-red')

const dadosParaExportar = computed(() => {
  if (!resLiquidez.value) return {}
  return {
    liquidez: resLiquidez.value,
    rentabilidade: resRentabilidade.value,
    endividamento: resEndividamento.value,
    atividade: resAtividade.value
  }
})
</script>

<template>
  <ModuleLayout titulo="Contabilidade" emoji="💰" :itensMenu="menuContabilidade">
    
    <div class="header-pagina">
      <h2>Dashboard Financeiro</h2>
      <p>Análise de performance e saúde financeira da empresa.</p>
    </div>

    <div class="control-panel">
      
      <div class="panel-section main-inputs">
        <div class="section-title">📅 Período de Análise (Obrigatório)</div>
        <div class="inputs-row">
          <div class="input-group">
            <label>Balanço Patrimonial (Final)</label>
            <div class="select-wrapper">
              <select v-model="selecionadoBalanco">
                <option value="" disabled>Selecione o arquivo...</option>
                <option v-for="(item, index) in historicoBalanco" :key="index" :value="index">
                  {{ item.data }} | Total: R$ {{ item.total.toLocaleString('pt-BR') }}
                </option>
              </select>
            </div>
          </div>
          
          <div class="input-group">
            <label>DRE do Exercício</label>
            <div class="select-wrapper">
              <select v-model="selecionadoDRE">
                <option value="" disabled>Selecione o arquivo...</option>
                <option v-for="(item, index) in historicoDRE" :key="index" :value="index">
                  {{ item.data }} | Lucro: R$ {{ item.lucro.toLocaleString('pt-BR') }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div class="panel-divider"></div>

      <div class="panel-section secondary-inputs">
        <div class="section-title">⚖️ Comparativo (Para Médias)</div>
        <div class="input-group">
          <label>Balanço Anterior (Inicial)</label>
          <div class="select-wrapper">
            <select v-model="selecionadoBalancoAnt">
              <option value="">Não utilizar (Cálculo Simples)</option>
              <option v-for="(item, index) in historicoBalanco" :key="index" :value="index">
                {{ item.data }} | Total: R$ {{ item.total.toLocaleString('pt-BR') }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <div class="panel-actions">
        <button @click="calcularIndices" class="btn-primary" :disabled="loading">
          {{ loading ? 'Calculando...' : 'Gerar Dashboard' }}
        </button>
        <BtnExcel v-if="resLiquidez" :dados="dadosParaExportar" tipo="indicadores" class="btn-secondary"/>
      </div>
      
    </div>

    <div v-if="erro" class="msg-erro">{{ erro }}</div>

    <div v-if="resLiquidez" class="dashboard-grid">
      
      <div class="kpi-card liquidity">
        <div class="card-header">
          <h3>💧 Liquidez</h3>
          <span class="badge">Solvência</span>
        </div>
        <div class="kpi-content">
          <div class="kpi-item">
            <span class="label">Corrente</span>
            <strong :class="getClassLiq(resLiquidez.indices.corrente)">{{ resLiquidez.indices.corrente }}</strong>
            <small>Ativo Circ. / Passivo Circ.</small>
          </div>
          <div class="kpi-item">
            <span class="label">Seca</span>
            <strong :class="getClassLiq(resLiquidez.indices.seca)">{{ resLiquidez.indices.seca }}</strong>
            <small>Sem Estoques</small>
          </div>
          <div class="kpi-item">
            <span class="label">Imediata</span>
            <strong :class="getClassLiq(resLiquidez.indices.imediata)">{{ resLiquidez.indices.imediata }}</strong>
            <small>Disponível / PC</small>
          </div>
          <div class="kpi-item">
            <span class="label">Geral</span>
            <strong :class="getClassLiq(resLiquidez.indices.geral)">{{ resLiquidez.indices.geral }}</strong>
            <small>Longo Prazo</small>
          </div>
        </div>
      </div>

      <div class="kpi-card profitability">
        <div class="card-header">
          <h3>📈 Rentabilidade</h3>
          <span class="badge" v-if="resRentabilidade.meta_dados.usou_media">Média ✅</span>
          <span class="badge warning" v-else>Simples ⚠️</span>
        </div>
        <div class="kpi-content">
          <div class="kpi-item highlight">
            <span class="label">ROI</span>
            <strong :class="getClassRent(resRentabilidade.indices.roi)">{{ resRentabilidade.indices.roi }}%</strong>
            <small>Retorno s/ Investimento</small>
          </div>
          <div class="kpi-item">
            <span class="label">ROE</span>
            <strong :class="getClassRent(resRentabilidade.indices.roe)">{{ resRentabilidade.indices.roe }}%</strong>
            <small>Retorno s/ PL</small>
          </div>
          <div class="kpi-item">
            <span class="label">ROA</span>
            <strong :class="getClassRent(resRentabilidade.indices.roa)">{{ resRentabilidade.indices.roa }}%</strong>
            <small>Retorno s/ Ativo</small>
          </div>
        </div>
      </div>

      <div class="kpi-card activity">
        <div class="card-header">
          <h3>🔄 Ciclos (Dias)</h3>
          <span class="badge" v-if="resAtividade.meta_dados.usou_media">Média ✅</span>
          <span class="badge warning" v-else>Simples ⚠️</span>
        </div>
        <div class="kpi-content">
          <div class="kpi-item">
            <span class="label">PME (Estoque)</span>
            <strong>{{ resAtividade.indices.pme }}</strong>
          </div>
          <div class="kpi-item">
            <span class="label">PMR (Receber)</span>
            <strong>{{ resAtividade.indices.pmr }}</strong>
          </div>
          <div class="kpi-item">
            <span class="label">PMP (Pagar)</span>
            <strong>{{ resAtividade.indices.pmp }}</strong>
          </div>
        </div>
        <div class="cycle-footer">
          <div class="cycle-item">
            <span>Ciclo Operacional:</span>
            <strong>{{ resAtividade.indices.ciclo_operacional }} dias</strong>
          </div>
          <div class="cycle-item caixa" :class="getClassCiclo(resAtividade.indices.ciclo_caixa)">
            <span>Ciclo de Caixa:</span>
            <strong>{{ resAtividade.indices.ciclo_caixa }} dias</strong>
          </div>
        </div>
      </div>

      <div class="kpi-card structure">
        <div class="card-header">
          <h3>⚖️ Estrutura</h3>
          <span class="badge">Capital</span>
        </div>
        <div class="kpi-content">
          <div class="kpi-item large">
            <span class="label">Terceiros / Próprio</span>
            <strong>{{ resEndividamento.indices.ct_cp }}x</strong>
            <small>Dívida para cada R$1 próprio</small>
          </div>
          <div class="kpi-item large">
            <span class="label">Part. Terceiros</span>
            <strong :class="getClassEndiv(resEndividamento.indices.participacao_ct)">{{ resEndividamento.indices.participacao_ct }}%</strong>
            <small>Dependência externa</small>
          </div>
        </div>
      </div>

    </div>
  </ModuleLayout>
</template>

<style scoped>
/* CABEÇALHO */
.header-pagina { text-align: center; margin-bottom: 30px; }
.header-pagina h2 { color: #2c3e50; margin: 0; font-size: 1.8rem; }
.header-pagina p { color: #7f8c8d; margin-top: 5px; }

/* --- PAINEL DE CONTROLE (NOVO) --- */
.control-panel {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  padding: 20px;
  margin-bottom: 40px;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: flex-end;
  border: 1px solid #edf2f7;
}

.panel-section { flex: 1; min-width: 250px; }
.section-title { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; color: #718096; font-weight: 700; margin-bottom: 12px; }

.inputs-row { display: flex; gap: 15px; }
.input-group { flex: 1; }
.input-group label { display: block; font-size: 0.9rem; color: #4a5568; margin-bottom: 6px; font-weight: 500; }

.select-wrapper select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  background: #fff;
  font-size: 0.95rem;
  color: #2d3748;
  transition: border 0.2s;
}
.select-wrapper select:focus { border-color: #4299e1; outline: none; box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1); }

.panel-divider { width: 1px; background: #e2e8f0; margin: 0 10px; align-self: stretch; }

.panel-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 180px;
}

.btn-primary { background: #2c3e50; color: white; padding: 12px; border-radius: 6px; border: none; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-primary:hover { background: #34495e; transform: translateY(-1px); }
.btn-primary:disabled { background: #cbd5e0; cursor: not-allowed; }

.btn-secondary { width: 100%; justify-content: center; font-size: 0.9rem; padding: 10px; }

/* MENSAGEM DE ERRO */
.msg-erro { background: #fff5f5; color: #c53030; padding: 15px; border-radius: 8px; margin-bottom: 30px; text-align: center; border: 1px solid #fed7d7; }

/* --- GRID DO DASHBOARD (NOVO) --- */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

/* CARDS */
.kpi-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02);
  display: flex;
  flex-direction: column;
}

/* Header Colorido */
.card-header { padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; }
.card-header h3 { margin: 0; font-size: 1.1rem; font-weight: 700; color: #2d3748; display: flex; align-items: center; gap: 8px; }

/* Cores dos Headers */
.liquidity .card-header { background: linear-gradient(to right, #ebf8ff, #fff); border-left: 5px solid #4299e1; }
.profitability .card-header { background: linear-gradient(to right, #f0fff4, #fff); border-left: 5px solid #48bb78; }
.activity .card-header { background: linear-gradient(to right, #faf5ff, #fff); border-left: 5px solid #9f7aea; }
.structure .card-header { background: linear-gradient(to right, #fffaf0, #fff); border-left: 5px solid #ed8936; }

.badge { font-size: 0.75rem; background: #e2e8f0; color: #4a5568; padding: 3px 8px; border-radius: 12px; font-weight: 600; }
.badge.warning { background: #feebc8; color: #c05621; }

/* Conteúdo dos KPIs */
.kpi-content { padding: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; flex-grow: 1; }
.kpi-item { display: flex; flex-direction: column; align-items: center; text-align: center; }
.kpi-item.large { grid-column: span 1; } 

.kpi-item .label { font-size: 0.8rem; color: #a0aec0; text-transform: uppercase; font-weight: 600; margin-bottom: 4px; }
.kpi-item strong { font-size: 1.6rem; color: #2d3748; font-weight: 800; line-height: 1.2; }
.kpi-item small { font-size: 0.75rem; color: #cbd5e0; margin-top: 2px; }

/* Footer de Ciclos */
.cycle-footer { background: #f7fafc; padding: 15px; border-top: 1px solid #edf2f7; display: flex; flex-direction: column; gap: 8px; }
.cycle-item { display: flex; justify-content: space-between; font-size: 0.9rem; color: #4a5568; }
.cycle-item strong { color: #2d3748; }
.cycle-item.caixa { margin-top: 5px; padding-top: 8px; border-top: 1px dashed #cbd5e0; font-weight: bold; }
.cycle-item.caixa.text-green { color: #27ae60; }
.cycle-item.caixa.text-red { color: #e53e3e; }

/* Cores de Texto */
.text-green { color: #38a169; }
.text-orange { color: #dd6b20; }
.text-red { color: #e53e3e; }

/* Responsividade */
@media (max-width: 900px) {
  .control-panel { flex-direction: column; align-items: stretch; }
  .panel-divider { height: 1px; width: 100%; margin: 15px 0; }
  .inputs-row { flex-direction: column; }
}
</style>