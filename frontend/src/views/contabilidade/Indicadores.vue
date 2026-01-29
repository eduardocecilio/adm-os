<script setup>
import { ref, onMounted, computed } from 'vue' // <--- Adicionei 'computed'
import ModuleLayout from '../../components/ModuleLayout.vue'
import BtnExcel from '../../components/BtnExcel.vue' // <--- Importei o Botão
import { menuContabilidade } from '../../constants/menus/menuContabilidade.js'

// --- Estados ---
const historicoBalanco = ref([])
const historicoDRE = ref([])

const selecionadoBalanco = ref('') 
const selecionadoDRE = ref('')     

const resLiquidez = ref(null)
const resRentabilidade = ref(null)
const resEndividamento = ref(null)
const resAtividade = ref(null)

const loading = ref(false)
const erro = ref(null)

// --- Carregar Dados do LocalStorage ---
onMounted(() => {
  const savedBalanco = localStorage.getItem('historico_balanco')
  const savedDRE = localStorage.getItem('historico_dre')

  if (savedBalanco) historicoBalanco.value = JSON.parse(savedBalanco)
  if (savedDRE) historicoDRE.value = JSON.parse(savedDRE)
})

// --- Computed para Exportação (Junta tudo num pacote só) ---
const dadosParaExportar = computed(() => {
  // Só libera se tiver calculado tudo
  if (!resLiquidez.value || !resRentabilidade.value || !resEndividamento.value || !resAtividade.value) {
    return null
  }
  return {
    liquidez: resLiquidez.value,
    rentabilidade: resRentabilidade.value,
    endividamento: resEndividamento.value,
    atividade: resAtividade.value
  }
})

// --- Ação de Calcular ---
const calcularIndices = async () => {
  erro.value = null
  resLiquidez.value = null
  resRentabilidade.value = null
  resEndividamento.value = null
  resAtividade.value = null

  if (selecionadoBalanco.value === '' || selecionadoDRE.value === '') {
    erro.value = "⚠️ Por favor, selecione um Balanço e uma DRE."
    return
  }

  const balancoObj = historicoBalanco.value[selecionadoBalanco.value].dados
  const dreObj = historicoDRE.value[selecionadoDRE.value].dados

  loading.value = true

  try {
    const headers = { 'Content-Type': 'application/json', 'x-token': 'admin-os-segredo-2026' }
    const body = JSON.stringify({ balanco: balancoObj, dre: dreObj })

    // 4 CHAMADAS PARALELAS
    const [respLiq, respRent, respEnd, respAtiv] = await Promise.all([
      fetch('http://127.0.0.1:8000/contabilidade/indicadores/liquidez', { method: 'POST', headers, body }),
      fetch('http://127.0.0.1:8000/contabilidade/indicadores/rentabilidade', { method: 'POST', headers, body }),
      fetch('http://127.0.0.1:8000/contabilidade/indicadores/endividamento', { method: 'POST', headers, body }),
      fetch('http://127.0.0.1:8000/contabilidade/indicadores/atividade', { method: 'POST', headers, body })
    ])

    if (!respLiq.ok || !respRent.ok || !respEnd.ok || !respAtiv.ok) throw new Error("Erro no servidor.")

    resLiquidez.value = await respLiq.json()
    resRentabilidade.value = await respRent.json()
    resEndividamento.value = await respEnd.json()
    resAtividade.value = await respAtiv.json()

  } catch (e) {
    console.error(e)
    erro.value = "Erro: " + e.message
  } finally {
    loading.value = false
  }
}

// Helpers de classe (Cores)
const getClassLiq = (v) => v > 1.0 ? 'bom' : (v >= 0.9 ? 'medio' : 'ruim')
const getClassRent = (v) => v > 15.0 ? 'bom' : (v > 5.0 ? 'medio' : 'ruim')
const getClassEndiv = (v) => v < 50.0 ? 'bom' : (v < 70.0 ? 'medio' : 'ruim')
const getClassCiclo = (v) => v < 60 ? 'bom' : (v < 90 ? 'medio' : 'ruim')
</script>

<template>
  <ModuleLayout titulo="Contabilidade" emoji="💰" :itensMenu="menuContabilidade">
    
    <div class="header-pagina">
      <h2>Indicadores Financeiros</h2>
      <p>Dashboard completo de performance empresarial.</p>
    </div>

    <div class="painel-selecao">
      <div class="campo-select">
        <label>1. Escolha o Balanço Patrimonial</label>
        <select v-model="selecionadoBalanco" class="input-select">
          <option value="" disabled>Selecione...</option>
          <option v-for="(item, index) in historicoBalanco" :key="index" :value="index">
            📅 {{ item.data }} - Total: R$ {{ item.total.toLocaleString('pt-BR') }}
          </option>
        </select>
      </div>
      <div class="campo-select">
        <label>2. Escolha a DRE</label>
        <select v-model="selecionadoDRE" class="input-select">
          <option value="" disabled>Selecione...</option>
          <option v-for="(item, index) in historicoDRE" :key="index" :value="index">
            📅 {{ item.data }} - Lucro: R$ {{ item.lucro.toLocaleString('pt-BR') }}
          </option>
        </select>
      </div>

      <div class="actions-row">
        <button @click="calcularIndices" class="btn-calcular" :disabled="loading">
          {{ loading ? 'Calculando...' : '📊 Gerar Dashboard' }}
        </button>

        <BtnExcel 
          v-if="dadosParaExportar"
          :dados="dadosParaExportar" 
          tipo="indicadores" 
          nomeArquivo="Relatorio_Indicadores.xlsx"
          class="btn-exportar"
        />
      </div>

      <div v-if="erro" class="msg-erro">{{ erro }}</div>
    </div>

    <div v-if="resLiquidez && resRentabilidade && resEndividamento && resAtividade" class="resultados-grid">
      
      <div class="card-resultado">
        <h3>💧 Liquidez</h3>
        <div class="indices-list">
          <div class="item-indice"><span class="label">Corrente</span><div class="valor" :class="getClassLiq(resLiquidez.indices.corrente)">{{ resLiquidez.indices.corrente }}</div></div>
          <div class="item-indice"><span class="label">Seca</span><div class="valor" :class="getClassLiq(resLiquidez.indices.seca)">{{ resLiquidez.indices.seca }}</div></div>
          <div class="item-indice"><span class="label">Imediata</span><div class="valor" :class="getClassLiq(resLiquidez.indices.imediata)">{{ resLiquidez.indices.imediata }}</div></div>
          <div class="item-indice"><span class="label">Geral</span><div class="valor" :class="getClassLiq(resLiquidez.indices.geral)">{{ resLiquidez.indices.geral }}</div></div>
        </div>
      </div>

      <div class="card-resultado">
        <h3>📈 Rentabilidade</h3>
        <div class="indices-list">
          <div class="item-indice"><span class="label">ROI</span><div class="valor" :class="getClassRent(resRentabilidade.indices.roi)">{{ resRentabilidade.indices.roi }}%</div></div>
          <div class="item-indice"><span class="label">ROE</span><div class="valor" :class="getClassRent(resRentabilidade.indices.roe)">{{ resRentabilidade.indices.roe }}%</div></div>
          <div class="item-indice"><span class="label">ROA</span><div class="valor" :class="getClassRent(resRentabilidade.indices.roa)">{{ resRentabilidade.indices.roa }}%</div></div>
        </div>
      </div>

      <div class="card-resultado">
        <h3>⚖️ Estrutura</h3>
        <div class="indices-list">
          <div class="item-indice full-width"><span class="label">CT / CP</span><div class="valor">{{ resEndividamento.indices.ct_cp }}</div></div>
          <div class="item-indice full-width"><span class="label">Part. Terceiros</span><div class="valor" :class="getClassEndiv(resEndividamento.indices.participacao_ct)">{{ resEndividamento.indices.participacao_ct }}%</div></div>
        </div>
      </div>

      <div class="card-resultado">
        <h3>🔄 Ciclos de Atividade</h3>
        <div class="indices-list">
          
          <div class="item-indice">
            <span class="label">PME (Estocagem)</span>
            <div class="valor">{{ resAtividade.indices.pme }} <small>dias</small></div>
          </div>
          <div class="item-indice">
            <span class="label">PMR (Recebimento)</span>
            <div class="valor">{{ resAtividade.indices.pmr }} <small>dias</small></div>
          </div>
          <div class="item-indice">
            <span class="label">PMP (Pagamento)</span>
            <div class="valor">{{ resAtividade.indices.pmp }} <small>dias</small></div>
          </div>
          
          <div class="item-indice highlight-blue">
            <span class="label">Ciclo Operacional</span>
            <div class="valor">{{ resAtividade.indices.ciclo_operacional }} <small>dias</small></div>
          </div>

          <div class="item-indice full-width highlight-green">
            <span class="label">Ciclo de Caixa</span>
            <div class="valor" :class="getClassCiclo(resAtividade.indices.ciclo_caixa)">
              {{ resAtividade.indices.ciclo_caixa }} dias
            </div>
            <p class="desc">Tempo entre pagar fornecedor e receber do cliente.</p>
          </div>

        </div>
      </div>

    </div>
  </ModuleLayout>
</template>

<style scoped>
.header-pagina { text-align: center; margin-bottom: 30px; }
.painel-selecao { background: white; padding: 30px; border-radius: 12px; border: 1px solid #e0e0e0; max-width: 600px; margin: 0 auto 40px auto; }
.campo-select { margin-bottom: 20px; }
.input-select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; }

/* Nova linha de botões */
.actions-row { display: flex; gap: 15px; align-items: center; }
.btn-calcular { flex: 2; padding: 15px; background: #2c3e50; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; font-size: 1rem; }
.btn-calcular:hover { background: #34495e; transform: translateY(-2px); }
.btn-exportar { flex: 1; height: 49px; justify-content: center; } /* Ajuste de altura */

.msg-erro { margin-top: 15px; color: #c0392b; background: #ffeaea; padding: 10px; border-radius: 6px; text-align: center; }

/* Grid de Resultados */
.resultados-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; align-items: start; }
.card-resultado { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; height: 100%; box-sizing: border-box; }
.card-resultado h3 { margin-top: 0; color: #2c3e50; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px; margin-bottom: 15px; font-size: 1.1rem; }
.indices-list { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
.item-indice { text-align: center; background: #f9f9f9; padding: 10px; border-radius: 8px; }
.item-indice.full-width { grid-column: span 2; }
.item-indice .label { display: block; font-size: 0.8rem; color: #7f8c8d; font-weight: 600; text-transform: uppercase; }
.item-indice .valor { font-size: 1.4rem; font-weight: 800; color: #2c3e50; }
.item-indice .valor small { font-size: 0.8rem; font-weight: 400; color: #7f8c8d; }

.highlight-blue { background: #ebf8ff; border: 1px solid #bee3f8; }
.highlight-green { background: #f0fff4; border: 1px solid #c6f6d5; }

.valor.bom { color: #27ae60; }
.valor.medio { color: #f39c12; }
.valor.ruim { color: #c0392b; }

@media (max-width: 600px) { .indices-list { grid-template-columns: 1fr; } .item-indice.full-width { grid-column: span 1; } }
</style>