<script setup>
import { ref, onMounted, computed } from 'vue'
import ModuleLayout from '../../components/ModuleLayout.vue'
import BtnExcel from '../../components/BtnExcel.vue'
import ModalGrafico from '../../components/ModalGrafico.vue'
import { menuContabilidade } from '../../constants/menus/menuContabilidade.js'

// --- ESTADOS ---
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
const dashboardGerado = ref(false)

// Dados para Evolução (Agora controlados pela seleção)
const evolucao = ref({
  ativo: { valor: 0, history: [] },
  passivo: { valor: 0, history: [] },
  pl: { valor: 0, history: [] }
})

const modalAberto = ref(false)
const dadosModal = ref({ titulo: '', valor: '', variacao: 0, history: [] })

onMounted(() => {
  const savedBalanco = localStorage.getItem('historico_balanco')
  const savedDRE = localStorage.getItem('historico_dre')
  if (savedBalanco) historicoBalanco.value = JSON.parse(savedBalanco)
  if (savedDRE) historicoDRE.value = JSON.parse(savedDRE)
})

const somarGrupo = (lista) => {
  if (!lista || !Array.isArray(lista)) return 0
  return lista.reduce((acc, item) => acc + (Number(item.valor) || 0), 0)
}

// --- CÁLCULO (CORRIGIDO PARA ORDEM ANTERIOR -> ATUAL) ---
const calcularIndices = async () => {
  erro.value = null
  resLiquidez.value = null
  dashboardGerado.value = false

  if (selecionadoBalanco.value === '' || selecionadoDRE.value === '') {
    erro.value = "⚠️ Por favor, selecione os dados do Período Atual."
    return
  }

  // Objetos Selecionados
  const balancoObj = historicoBalanco.value[selecionadoBalanco.value].dados
  const dreObj = historicoDRE.value[selecionadoDRE.value].dados
  let balancoAntObj = null
  
  // 1. CONSTRUÇÃO DOS GRÁFICOS DE EVOLUÇÃO
  // A lógica agora respeita estritamente: [Valor Anterior, Valor Atual]
  const histAtivo = []
  const histPassivo = []
  const histPL = []

  // Se tiver Balanço Anterior selecionado, ele entra PRIMEIRO (Esquerda do gráfico)
  if (selecionadoBalancoAnt.value !== '') {
    balancoAntObj = historicoBalanco.value[selecionadoBalancoAnt.value].dados
    
    const antAtivo = somarGrupo(balancoAntObj.ativo_circulante) + somarGrupo(balancoAntObj.ativo_nao_circulante)
    const antPassivo = somarGrupo(balancoAntObj.passivo_circulante) + somarGrupo(balancoAntObj.passivo_nao_circulante)
    const antPL = somarGrupo(balancoAntObj.patrimonio_liquido)
    
    histAtivo.push(antAtivo)
    histPassivo.push(antPassivo)
    histPL.push(antPL)
  }

  // O Balanço Atual entra SEMPRE POR ÚLTIMO (Direita do gráfico)
  const atualAtivo = somarGrupo(balancoObj.ativo_circulante) + somarGrupo(balancoObj.ativo_nao_circulante)
  const atualPassivo = somarGrupo(balancoObj.passivo_circulante) + somarGrupo(balancoObj.passivo_nao_circulante)
  const atualPL = somarGrupo(balancoObj.patrimonio_liquido)

  histAtivo.push(atualAtivo)
  histPassivo.push(atualPassivo)
  histPL.push(atualPL)

  // Atualiza estado da evolução
  evolucao.value = {
    ativo: { valor: atualAtivo, history: histAtivo },
    passivo: { valor: atualPassivo, history: histPassivo },
    pl: { valor: atualPL, history: histPL }
  }

loading.value = true

  try {
    // 1. URL Dinâmica com Fallback
    const baseURL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001';
    
    // 2. Headers Centralizados
    const headers = { 
      'Content-Type': 'application/json', 
      'x-token': 'seu_token_secreto' 
    }
    const body = JSON.stringify({ balanco: balancoObj, dre: dreObj, balanco_anterior: balancoAntObj })

    // 3. Chamadas Paralelas
    const [rL, rR, rE, rA] = await Promise.all([
      fetch(`${baseURL}/contabilidade/indicadores/liquidez`, { method: 'POST', headers, body }),
      fetch(`${baseURL}/contabilidade/indicadores/rentabilidade`, { method: 'POST', headers, body }),
      fetch(`${baseURL}/contabilidade/indicadores/endividamento`, { method: 'POST', headers, body }),
      fetch(`${baseURL}/contabilidade/indicadores/atividade`, { method: 'POST', headers, body })
    ])

    // 4. Verificação de Integridade (Se o Token falhar, o status será 401)
    if (!rL.ok) {
      if (rL.status === 401) throw new Error("Acesso não autorizado (Token inválido)");
      throw new Error(`Erro no Backend (Status: ${rL.status})`);
    }

    // 5. Atribuição dos resultados
    resLiquidez.value = await rL.json()
    resRentabilidade.value = await rR.json()
    resEndividamento.value = await rE.json()
    resAtividade.value = await rA.json()
    
    dashboardGerado.value = true

  } catch (e) {
    console.error("Erro no fetch de indicadores:", e)
    erro.value = "Erro: " + e.message
  } finally {
    loading.value = false
  }
}

// Modal
const abrirGraficoEvolucao = (titulo, objDados) => {
  let history = objDados.history || []
  if (history.length < 2) history = [objDados.valor, objDados.valor]

  dadosModal.value = {
    titulo: titulo,
    valor: formatMoney(objDados.valor),
    variacao: 0, 
    history: history
  }
  modalAberto.value = true
}

// Utils Gráfico (Sparkline)
const getMiniSvgPath = (dataPoints) => {
  if (!dataPoints || dataPoints.length < 2) return ""
  const width = 200
  const height = 50
  const min = Math.min(...dataPoints)
  const max = Math.max(...dataPoints)
  const range = max - min || 1
  
  if (range === 0) return `M 0 ${height/2} L ${width} ${height/2}`

  const stepX = width / (dataPoints.length - 1)
  let path = `M 0 ${height - ((dataPoints[0] - min) / range) * height}`
  
  dataPoints.forEach((val, i) => {
    if (i === 0) return
    const x = i * stepX
    const y = height - ((val - min) / range) * height
    path += ` L ${x} ${y}`
  })
  return path
}

// Helpers
const getClassLiq = (v) => v > 1.0 ? 'text-green' : (v >= 0.9 ? 'text-orange' : 'text-red')
const getClassRent = (v) => v > 15.0 ? 'text-green' : (v > 5.0 ? 'text-orange' : 'text-red')
const getClassEndiv = (v) => v < 50.0 ? 'text-green' : (v < 70.0 ? 'text-orange' : 'text-red')
const getClassCiclo = (v) => v < 60 ? 'text-green' : (v < 90 ? 'text-orange' : 'text-red')
const formatMoney = (v) => 'R$ ' + v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })

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
    
    <ModalGrafico 
      :show="modalAberto" 
      :titulo="dadosModal.titulo" 
      :dados="dadosModal"
      :exibirPeriodos="false" 
      @close="modalAberto = false" 
    />

    <div class="header-pagina">
      <h2>Dashboard Financeiro</h2>
      <p>Análise de performance e saúde financeira da empresa.</p>
    </div>

    <div class="control-panel">
      <div class="panel-section main-inputs">
        <div class="section-title">📅 Período de Análise</div>
        <div class="inputs-row">
          <div class="input-group">
            <label>Balanço Patrimonial</label>
            <div class="select-wrapper">
              <select v-model="selecionadoBalanco">
                <option value="" disabled>Selecione...</option>
                <option v-for="(item, index) in historicoBalanco" :key="index" :value="index">{{ item.data }} - Total: {{ item.total.toLocaleString('pt-BR') }}</option>
              </select>
            </div>
          </div>
          <div class="input-group">
            <label>DRE</label>
            <div class="select-wrapper">
              <select v-model="selecionadoDRE">
                <option value="" disabled>Selecione...</option>
                <option v-for="(item, index) in historicoDRE" :key="index" :value="index">{{ item.data }} - Lucro: {{ item.lucro.toLocaleString('pt-BR') }}</option>
              </select>
            </div>
          </div>
        </div>
      </div>
      
      <div class="panel-section secondary-inputs" style="border-left:1px solid #eee; padding-left:20px;">
        <div class="section-title">⚖️ Comparativo (Opcional)</div>
        <div class="input-group">
          <label>Balanço Anterior</label>
          <div class="select-wrapper">
            <select v-model="selecionadoBalancoAnt">
              <option value="">Não usar média</option>
              <option v-for="(item, index) in historicoBalanco" :key="index" :value="index">{{ item.data }}</option>
            </select>
          </div>
        </div>
      </div>

      <div class="panel-actions">
        <button @click="calcularIndices" class="btn-primary" :disabled="loading">{{ loading ? 'Calculando...' : 'Gerar Dashboard' }}</button>
        <BtnExcel v-if="resLiquidez" :dados="dadosParaExportar" tipo="indicadores" class="btn-secondary"/>
      </div>
    </div>

    <div v-if="erro" class="msg-erro">{{ erro }}</div>

    <div v-if="dashboardGerado" class="section-evolution">
      <h3 class="section-header">🏛️ Evolução Patrimonial</h3>
      <div class="evolution-grid">
        
        <div class="evo-card blue clickable" @click="abrirGraficoEvolucao('Evolução do Ativo Total', evolucao.ativo)">
          <div class="evo-content-clean">
            <span class="evo-label">Ativo Total</span>
            <div class="evo-chart">
              <svg width="100%" height="100%" viewBox="0 0 200 50" preserveAspectRatio="none">
                <path :d="getMiniSvgPath(evolucao.ativo.history)" fill="none" stroke="#3498db" stroke-width="2" />
              </svg>
            </div>
          </div>
        </div>

        <div class="evo-card red clickable" @click="abrirGraficoEvolucao('Evolução do Passivo Exigível', evolucao.passivo)">
          <div class="evo-content-clean">
            <span class="evo-label">Passivo Total</span>
            <div class="evo-chart">
              <svg width="100%" height="100%" viewBox="0 0 200 50" preserveAspectRatio="none">
                <path :d="getMiniSvgPath(evolucao.passivo.history)" fill="none" stroke="#e74c3c" stroke-width="2" />
              </svg>
            </div>
          </div>
        </div>

        <div class="evo-card green clickable" @click="abrirGraficoEvolucao('Evolução do Patrimônio Líquido', evolucao.pl)">
          <div class="evo-content-clean">
            <span class="evo-label">Patrimônio Líquido</span>
            <div class="evo-chart">
              <svg width="100%" height="100%" viewBox="0 0 200 50" preserveAspectRatio="none">
                <path :d="getMiniSvgPath(evolucao.pl.history)" fill="none" stroke="#27ae60" stroke-width="2" />
              </svg>
            </div>
          </div>
        </div>

      </div>
    </div>

    <div v-if="dashboardGerado" class="dashboard-grid mt-big">
      
      <div class="kpi-card liquidity">
        <div class="card-header"><h3>💧 Liquidez</h3><span class="badge">Solvência</span></div>
        <div class="kpi-content">
          <div class="kpi-item"><span class="label">Corrente</span><strong :class="getClassLiq(resLiquidez.indices.corrente)">{{ resLiquidez.indices.corrente }}</strong></div>
          <div class="kpi-item"><span class="label">Seca</span><strong :class="getClassLiq(resLiquidez.indices.seca)">{{ resLiquidez.indices.seca }}</strong></div>
          <div class="kpi-item"><span class="label">Imediata</span><strong :class="getClassLiq(resLiquidez.indices.imediata)">{{ resLiquidez.indices.imediata }}</strong></div>
          <div class="kpi-item"><span class="label">Geral</span><strong :class="getClassLiq(resLiquidez.indices.geral)">{{ resLiquidez.indices.geral }}</strong></div>
        </div>
      </div>

      <div class="kpi-card profitability">
        <div class="card-header"><h3>📈 Rentabilidade</h3><span class="badge" v-if="resRentabilidade.meta_dados.usou_media">Média ✅</span><span class="badge warning" v-else>Simples ⚠️</span></div>
        <div class="kpi-content">
          <div class="kpi-item highlight"><span class="label">ROI</span><strong :class="getClassRent(resRentabilidade.indices.roi)">{{ resRentabilidade.indices.roi }}%</strong></div>
          <div class="kpi-item"><span class="label">ROE</span><strong :class="getClassRent(resRentabilidade.indices.roe)">{{ resRentabilidade.indices.roe }}%</strong></div>
          <div class="kpi-item"><span class="label">ROA</span><strong :class="getClassRent(resRentabilidade.indices.roa)">{{ resRentabilidade.indices.roa }}%</strong></div>
        </div>
      </div>

      <div class="kpi-card activity">
        <div class="card-header"><h3>🔄 Ciclos</h3><span class="badge" v-if="resAtividade.meta_dados.usou_media">Média ✅</span><span class="badge warning" v-else>Simples ⚠️</span></div>
        <div class="kpi-content">
          <div class="kpi-item"><span class="label">PME</span><strong>{{ resAtividade.indices.pme }}</strong></div>
          <div class="kpi-item"><span class="label">PMR</span><strong>{{ resAtividade.indices.pmr }}</strong></div>
          <div class="kpi-item"><span class="label">PMP</span><strong>{{ resAtividade.indices.pmp }}</strong></div>
        </div>
        <div class="cycle-footer">
          <div class="cycle-item"><span>Ciclo Operacional:</span><strong>{{ resAtividade.indices.ciclo_operacional }} dias</strong></div>
          <div class="cycle-item caixa" :class="getClassCiclo(resAtividade.indices.ciclo_caixa)"><span>Ciclo de Caixa:</span><strong>{{ resAtividade.indices.ciclo_caixa }} dias</strong></div>
        </div>
      </div>

      <div class="kpi-card structure">
        <div class="card-header"><h3>⚖️ Estrutura</h3><span class="badge">Capital</span></div>
        <div class="kpi-content">
          <div class="kpi-item large"><span class="label">CT / CP</span><strong>{{ resEndividamento.indices.ct_cp }}x</strong></div>
          <div class="kpi-item large"><span class="label">Part. Terceiros</span><strong :class="getClassEndiv(resEndividamento.indices.participacao_ct)">{{ resEndividamento.indices.participacao_ct }}%</strong></div>
        </div>
      </div>

    </div>
  </ModuleLayout>
</template>

<style scoped>
.header-pagina { text-align: center; margin-bottom: 30px; }
.control-panel { background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); padding: 20px; margin-bottom: 30px; display: flex; flex-wrap: wrap; gap: 20px; align-items: flex-end; border: 1px solid #edf2f7; }
.panel-section { flex: 1; min-width: 250px; }
.section-title { font-size: 0.85rem; text-transform: uppercase; font-weight: 700; margin-bottom: 12px; color: #718096; }
.inputs-row { display: flex; gap: 15px; }
.input-group { flex: 1; }
.input-group label { display: block; font-size: 0.9rem; margin-bottom: 6px; }
.select-wrapper select { width: 100%; padding: 10px; border: 1px solid #cbd5e0; border-radius: 6px; }
.panel-actions { display: flex; flex-direction: column; gap: 10px; min-width: 180px; }
.btn-primary { background: #2c3e50; color: white; padding: 12px; border-radius: 6px; border: none; font-weight: bold; cursor: pointer; }
.btn-secondary { width: 100%; justify-content: center; }
.msg-erro { background: #fff5f5; color: #c53030; padding: 15px; border-radius: 8px; margin-bottom: 30px; text-align: center; border: 1px solid #fed7d7; }

/* SEÇÃO EVOLUÇÃO (LIMPA) */
.section-evolution { margin-bottom: 40px; animation: fadeIn 0.5s ease-out; }
.section-header { font-size: 1.1rem; color: #718096; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; border-left: 4px solid #2c3e50; padding-left: 10px; }
.evolution-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }

.evo-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; position: relative; overflow: hidden; transition: transform 0.2s, box-shadow 0.2s; cursor: pointer; height: 100px; display: flex; align-items: center; justify-content: center; }
.evo-card:hover { transform: translateY(-3px); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }

.evo-content-clean { width: 100%; text-align: center; }
.evo-label { display: block; font-size: 1rem; color: #555; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; }
.evo-chart { width: 80%; height: 40px; margin: 0 auto; opacity: 0.8; }

.evo-card.blue { border-bottom: 4px solid #3498db; }
.evo-card.red { border-bottom: 4px solid #e74c3c; }
.evo-card.green { border-bottom: 4px solid #27ae60; }

/* INDICADORES */
.dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; animation: fadeIn 0.5s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.mt-big { margin-top: 40px; }

.kpi-card { background: white; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; display: flex; flex-direction: column; transition: 0.2s; }
.card-header { padding: 15px 20px; display: flex; justify-content: space-between; border-bottom: 1px solid #f0f0f0; }
.liquidity .card-header { background: linear-gradient(to right, #ebf8ff, #fff); border-left: 5px solid #4299e1; }
.profitability .card-header { background: linear-gradient(to right, #f0fff4, #fff); border-left: 5px solid #48bb78; }
.activity .card-header { background: linear-gradient(to right, #faf5ff, #fff); border-left: 5px solid #9f7aea; }
.structure .card-header { background: linear-gradient(to right, #fffaf0, #fff); border-left: 5px solid #ed8936; }
.badge { background: #e2e8f0; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; }
.badge.warning { background: #feebc8; color: #c05621; }
.kpi-content { padding: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.kpi-item { text-align: center; }
.kpi-item .label { display: block; font-size: 0.8rem; color: #a0aec0; text-transform: uppercase; font-weight: 600; }
.kpi-item strong { font-size: 1.6rem; color: #2d3748; }
.text-green { color: #38a169; } .text-orange { color: #dd6b20; } .text-red { color: #e53e3e; }
.cycle-footer { background: #f7fafc; padding: 15px; border-top: 1px solid #edf2f7; display: flex; flex-direction: column; gap: 8px; }
.cycle-item { display: flex; justify-content: space-between; font-size: 0.9rem; color: #4a5568; }
.cycle-item strong { color: #2d3748; }
.cycle-item.caixa { margin-top: 5px; padding-top: 8px; border-top: 1px dashed #cbd5e0; font-weight: bold; }

@media (max-width: 900px) { .control-panel { flex-direction: column; } .inputs-row { flex-direction: column; } }
</style>