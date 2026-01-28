<script setup>
import { ref, onMounted, computed } from 'vue'
import ModuleLayout from '../../components/ModuleLayout.vue'
import { menuContabilidade } from '../../constants/menus/menuContabilidade.js'

// --- Estados ---
const historicoBalanco = ref([])
const historicoDRE = ref([])

const selecionadoBalanco = ref('') // ID ou Index do balanço escolhido
const selecionadoDRE = ref('')     // ID ou Index da DRE escolhida

const resultado = ref(null)
const loading = ref(false)
const erro = ref(null)

// --- Carregar Dados do LocalStorage ---
onMounted(() => {
  const savedBalanco = localStorage.getItem('historico_balanco')
  const savedDRE = localStorage.getItem('historico_dre')

  if (savedBalanco) historicoBalanco.value = JSON.parse(savedBalanco)
  if (savedDRE) historicoDRE.value = JSON.parse(savedDRE)
})

// --- Ação de Calcular ---
const calcularIndices = async () => {
  erro.value = null
  resultado.value = null

  // 1. Validação Básica
  if (selecionadoBalanco.value === '' || selecionadoDRE.value === '') {
    erro.value = "⚠️ Por favor, selecione um Balanço e uma DRE do histórico para prosseguir."
    return
  }

  // 2. Recuperar os Objetos Reais
  // Como salvamos no localStorage como array, o value do select é o índice
  const balancoObj = historicoBalanco.value[selecionadoBalanco.value].dados
  const dreObj = historicoDRE.value[selecionadoDRE.value].dados

  loading.value = true

  try {
    // 3. Enviar para o Backend
    const response = await fetch('http://127.0.0.1:8000/contabilidade/indicadores/liquidez', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'x-token': 'admin-os-segredo-2026'
      },
      body: JSON.stringify({
        balanco: balancoObj,
        dre: dreObj
      })
    })

    if (!response.ok) {
      throw new Error("Erro no cálculo do servidor.")
    }

    const data = await response.json()
    resultado.value = data

  } catch (e) {
    erro.value = "Erro de conexão: " + e.message
  } finally {
    loading.value = false
  }
}

// --- Classificação Visual dos Índices ---
const getClass = (valor) => {
  if (valor > 1.0) return 'bom'
  if (valor >= 0.9) return 'medio'
  return 'ruim'
}
</script>

<template>
  <ModuleLayout titulo="Contabilidade" emoji="💰" :itensMenu="menuContabilidade">
    
    <div class="header-pagina">
      <h2>Indicadores Financeiros</h2>
      <p>Selecione as demonstrações salvas para gerar o relatório de performance.</p>
    </div>

    <div class="painel-selecao">
      
      <div class="campo-select">
        <label>1. Escolha o Balanço Patrimonial</label>
        <select v-model="selecionadoBalanco" class="input-select">
          <option value="" disabled>Selecione uma versão salva...</option>
          <option v-for="(item, index) in historicoBalanco" :key="index" :value="index">
            📅 {{ item.data }} - Total: R$ {{ item.total.toLocaleString('pt-BR') }}
          </option>
        </select>
        <small v-if="historicoBalanco.length === 0" class="aviso-vazio">Nenhum Balanço salvo no histórico.</small>
      </div>

      <div class="campo-select">
        <label>2. Escolha a DRE</label>
        <select v-model="selecionadoDRE" class="input-select">
          <option value="" disabled>Selecione uma versão salva...</option>
          <option v-for="(item, index) in historicoDRE" :key="index" :value="index">
            📅 {{ item.data }} - Lucro: R$ {{ item.lucro.toLocaleString('pt-BR') }}
          </option>
        </select>
        <small v-if="historicoDRE.length === 0" class="aviso-vazio">Nenhuma DRE salva no histórico.</small>
      </div>

      <button @click="calcularIndices" class="btn-calcular" :disabled="loading">
        {{ loading ? 'Calculando...' : '📊 Gerar Indicadores' }}
      </button>

      <div v-if="erro" class="msg-erro">{{ erro }}</div>
    </div>

    <div v-if="resultado" class="resultados-grid">
      
      <div class="card-resultado">
        <h3>💧 Índices de Liquidez</h3>
        <div class="indices-list">
          
          <div class="item-indice">
            <span class="label">Liquidez Corrente</span>
            <div class="valor" :class="getClass(resultado.indices.corrente)">
              {{ resultado.indices.corrente }}
            </div>
            <p class="desc">Capacidade de pagar dívidas de curto prazo.</p>
          </div>

          <div class="item-indice">
            <span class="label">Liquidez Seca</span>
            <div class="valor" :class="getClass(resultado.indices.seca)">
              {{ resultado.indices.seca }}
            </div>
            <p class="desc">Pagamento sem depender de vender estoque.</p>
          </div>

          <div class="item-indice">
            <span class="label">Liquidez Imediata</span>
            <div class="valor" :class="getClass(resultado.indices.imediata)">
              {{ resultado.indices.imediata }}
            </div>
            <p class="desc">Pagamento apenas com dinheiro em caixa.</p>
          </div>

          <div class="item-indice">
            <span class="label">Liquidez Geral</span>
            <div class="valor" :class="getClass(resultado.indices.geral)">
              {{ resultado.indices.geral }}
            </div>
            <p class="desc">Solvência a longo prazo.</p>
          </div>

        </div>
      </div>

      <div class="card-resultado blur">
        <h3>🏗️ Estrutura e Rentabilidade</h3>
        <p>Em breve: ROI, ROE, Margem EBITDA e Endividamento.</p>
      </div>

    </div>

  </ModuleLayout>
</template>

<style scoped>
.header-pagina { text-align: center; margin-bottom: 30px; }
.header-pagina h2 { color: #2c3e50; margin-bottom: 5px; }
.header-pagina p { color: #7f8c8d; }

/* Painel de Seleção */
.painel-selecao { 
  background: white; padding: 30px; border-radius: 12px; 
  border: 1px solid #e0e0e0; max-width: 600px; margin: 0 auto 40px auto; 
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.campo-select { margin-bottom: 20px; }
.campo-select label { display: block; font-weight: 600; color: #2c3e50; margin-bottom: 8px; }
.input-select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; background: white; font-size: 1rem; }
.aviso-vazio { color: #e74c3c; font-size: 0.85rem; margin-top: 5px; display: block; }

.btn-calcular { 
  width: 100%; padding: 15px; background: #2c3e50; color: white; border: none; 
  border-radius: 8px; font-size: 1.1rem; font-weight: bold; cursor: pointer; transition: 0.2s; 
}
.btn-calcular:hover { background: #34495e; transform: translateY(-2px); }
.btn-calcular:disabled { background: #95a5a6; cursor: not-allowed; }

.msg-erro { margin-top: 15px; color: #c0392b; background: #ffeaea; padding: 10px; border-radius: 6px; text-align: center; }

/* Grid de Resultados */
.resultados-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }

.card-resultado { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e0e0e0; }
.card-resultado h3 { margin-top: 0; color: #2c3e50; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px; margin-bottom: 20px; }

.indices-list { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.item-indice { text-align: center; background: #f9f9f9; padding: 15px; border-radius: 8px; }
.item-indice .label { display: block; font-size: 0.9rem; color: #7f8c8d; margin-bottom: 5px; }
.item-indice .valor { font-size: 2rem; font-weight: 800; margin-bottom: 5px; }
.item-indice .desc { font-size: 0.75rem; color: #95a5a6; line-height: 1.2; margin: 0; }

/* Cores Semânticas */
.valor.bom { color: #27ae60; }   /* Verde */
.valor.medio { color: #f39c12; } /* Amarelo */
.valor.ruim { color: #c0392b; }  /* Vermelho */

.blur { opacity: 0.5; filter: grayscale(1); pointer-events: none; }

@media (max-width: 600px) {
  .indices-list { grid-template-columns: 1fr; }
}
</style>