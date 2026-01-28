<script setup>
import { ref, computed, onMounted } from 'vue'
import ModuleLayout from '../../components/ModuleLayout.vue'
import DropdownEditable from '../../components/DropdownEditable.vue' // Nosso novo componente
import { menuContabilidade } from '../../constants/menus/menuContabilidade.js'
import { opcoesDRE } from '../../constants/options/contabilidade.js'

// --- Estrutura de Dados ---
const dre = ref({
  receita_bruta: [{ id: 1, conta: 'Venda de Serviços', valor: 0 }],
  deducoes: [{ id: 2, conta: 'Impostos sobre Vendas (ICMS/ISS)', valor: 0 }],
  custos: [{ id: 3, conta: 'CSP (Serviços)', valor: 0 }],
  despesas: [{ id: 4, conta: 'Salários e Encargos', valor: 0 }],
  resultado_financeiro: [{ id: 5, conta: 'Despesas Financeiras', valor: 0 }],
  impostos_lucro: [{ id: 6, conta: 'Simples Nacional', valor: 0 }]
})

const historico = ref([])

onMounted(() => {
  const saved = localStorage.getItem('historico_dre')
  if (saved) historico.value = JSON.parse(saved)
})

// --- Funções Auxiliares ---
const addLinha = (grupo) => {
  dre.value[grupo].push({ id: Date.now(), conta: '', valor: 0 })
}
const removeLinha = (grupo, index) => {
  dre.value[grupo].splice(index, 1)
}
const somar = (lista) => lista.reduce((acc, item) => acc + (Number(item.valor) || 0), 0)

// --- Cálculos ---
const totalReceitaBruta = computed(() => somar(dre.value.receita_bruta))
const totalDeducoes = computed(() => somar(dre.value.deducoes))
const receitaLiquida = computed(() => totalReceitaBruta.value - totalDeducoes.value)

const totalCustos = computed(() => somar(dre.value.custos))
const lucroBruto = computed(() => receitaLiquida.value - totalCustos.value)

const totalDespesas = computed(() => somar(dre.value.despesas))
const totalFinanceiro = computed(() => somar(dre.value.resultado_financeiro))

const lucroOperacional = computed(() => lucroBruto.value - totalDespesas.value)
const lucroAntesIR = computed(() => lucroOperacional.value + totalFinanceiro.value)

const totalImpostos = computed(() => somar(dre.value.impostos_lucro))
const lucroLiquido = computed(() => lucroAntesIR.value - totalImpostos.value)

const margemLiquida = computed(() => {
  if (totalReceitaBruta.value === 0) return 0
  return ((lucroLiquido.value / totalReceitaBruta.value) * 100).toFixed(1)
})

// --- Salvar ---
const salvarDRE = () => {
  const novo = {
    data: new Date().toLocaleString('pt-BR'),
    lucro: lucroLiquido.value,
    margem: margemLiquida.value,
    dados: JSON.parse(JSON.stringify(dre.value))
  }
  historico.value.unshift(novo)
  localStorage.setItem('historico_dre', JSON.stringify(historico.value))
  alert("✅ DRE salva com sucesso!")
}

const carregarVersao = (item) => {
  if(confirm('Carregar esta versão?')) {
    dre.value = JSON.parse(JSON.stringify(item.dados))
  }
}
const limparHistorico = () => {
  if(confirm('Limpar histórico?')) {
    historico.value = []
    localStorage.removeItem('historico_dre')
  }
}
</script>

<template>
  <ModuleLayout titulo="Contabilidade" emoji="💰" :itensMenu="menuContabilidade">
    
    <div class="header-pagina">
      <h2>DRE Gerencial</h2>
      <p>Demonstração do Resultado do Exercício.</p>
    </div>

    <div class="dre-container">
      
      <div class="section-block receita">
        <div class="section-header">
          <h3>(+) Receita Bruta</h3>
          <span>R$ {{ totalReceitaBruta.toFixed(2) }}</span>
        </div>
        <div v-for="(item, idx) in dre.receita_bruta" :key="item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.receita" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('receita_bruta', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('receita_bruta')" class="btn-add">+ Adicionar Receita</button>
      </div>

      <div class="section-block deducao">
        <div class="section-header">
          <h3>(-) Deduções da Receita</h3>
          <span>R$ {{ totalDeducoes.toFixed(2) }}</span>
        </div>
        <div v-for="(item, idx) in dre.deducoes" :key="item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.deducoes" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('deducoes', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('deducoes')" class="btn-add">+ Adicionar Dedução</button>
      </div>

      <div class="result-bar">
        <span>= Receita Líquida</span>
        <strong>R$ {{ receitaLiquida.toLocaleString('pt-BR', {minimumFractionDigits: 2}) }}</strong>
      </div>

      <div class="section-block custo">
        <div class="section-header">
          <h3>(-) Custos</h3>
          <span>R$ {{ totalCustos.toFixed(2) }}</span>
        </div>
        <div v-for="(item, idx) in dre.custos" :key="item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.custos" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('custos', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('custos')" class="btn-add">+ Adicionar Custo</button>
      </div>

      <div class="result-bar destaque">
        <span>= Lucro Bruto</span>
        <strong>R$ {{ lucroBruto.toLocaleString('pt-BR', {minimumFractionDigits: 2}) }}</strong>
      </div>

      <div class="section-block despesa">
        <div class="section-header">
          <h3>(-) Despesas Operacionais</h3>
          <span>R$ {{ totalDespesas.toFixed(2) }}</span>
        </div>
        <div v-for="(item, idx) in dre.despesas" :key="item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.despesas" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('despesas', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('despesas')" class="btn-add">+ Adicionar Despesa</button>
      </div>

      <div class="section-block financeiro">
        <div class="section-header">
          <h3>(+/-) Resultado Financeiro</h3>
          <span>R$ {{ totalFinanceiro.toFixed(2) }}</span>
        </div>
        <p class="hint">Negativo (-) para despesas, Positivo (+) para receitas.</p>
        <div v-for="(item, idx) in dre.resultado_financeiro" :key="item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.financeiro" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('resultado_financeiro', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('resultado_financeiro')" class="btn-add">+ Adicionar Financeiro</button>
      </div>

      <div class="section-block deducao">
        <div class="section-header">
          <h3>(-) Impostos s/ Lucro</h3>
          <span>R$ {{ totalImpostos.toFixed(2) }}</span>
        </div>
        <div v-for="(item, idx) in dre.impostos_lucro" :key="item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.impostos" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('impostos_lucro', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('impostos_lucro')" class="btn-add">+ Adicionar Imposto</button>
      </div>

      <div class="final-result">
        <div class="label">LUCRO LÍQUIDO DO EXERCÍCIO</div>
        <div class="value" :class="{ 'positive': lucroLiquido > 0, 'negative': lucroLiquido < 0 }">
          R$ {{ lucroLiquido.toLocaleString('pt-BR', {minimumFractionDigits: 2}) }}
        </div>
        <div class="margem">Margem Líquida: {{ margemLiquida }}%</div>
      </div>

      <div class="actions">
        <button class="btn-save" @click="salvarDRE">💾 Salvar DRE</button>
      </div>

      <div class="historico-box" v-if="historico.length">
        <div class="hist-head">
          <h4>Histórico</h4>
          <span @click="limparHistorico" class="clear-link">Limpar</span>
        </div>
        <div v-for="(h, i) in historico" :key="i" class="hist-row">
          <span>{{ h.data }}</span>
          <strong>R$ {{ h.lucro.toLocaleString('pt-BR') }} ({{ h.margem }}%)</strong>
          <button @click="carregarVersao(h)">Ver</button>
        </div>
      </div>

    </div>
  </ModuleLayout>
</template>

<style scoped>
.header-pagina { text-align: center; margin-bottom: 30px; }
.header-pagina h2 { color: #2c3e50; margin-bottom: 5px; }
.header-pagina p { color: #7f8c8d; }

.dre-container { max-width: 800px; margin: 0 auto 100px auto; }

/* Cards de Seção */
.section-block { background: white; padding: 20px; border-radius: 8px; border: 1px solid #edf2f7; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.section-header { display: flex; justify-content: space-between; margin-bottom: 10px; font-weight: 600; color: #4a5568; }
.receita .section-header { color: #38a169; }
.deducao .section-header, .custo .section-header, .despesa .section-header { color: #e53e3e; }

.line-row { display: grid; grid-template-columns: 3fr 1fr 30px; gap: 10px; margin-bottom: 8px; align-items: center; }
.input-valor { padding: 10px; border: 1px solid #e2e8f0; border-radius: 6px; text-align: right; font-family: monospace; font-weight: 600; height: 42px; box-sizing: border-box; }
.input-valor:focus { border-color: #4299e1; outline: none; }

.btn-del { border: none; background: none; color: #cbd5e0; font-size: 1.5rem; cursor: pointer; }
.btn-del:hover { color: #e53e3e; }
.btn-add { background: none; border: 1px dashed #cbd5e0; color: #718096; padding: 8px; width: 100%; border-radius: 6px; cursor: pointer; margin-top: 5px; transition: 0.2s; }
.btn-add:hover { border-color: #4299e1; color: #4299e1; background: #ebf8ff; }
.hint { font-size: 0.8rem; color: #a0aec0; margin-top: -5px; margin-bottom: 10px; font-style: italic; }

/* Barras de Resultado */
.result-bar { background: #f7fafc; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-radius: 8px; margin-bottom: 15px; font-weight: 500; color: #4a5568; border-left: 4px solid #cbd5e0; }
.result-bar.destaque { background: #edf2f7; border-left-color: #4a5568; font-size: 1.1rem; }

/* Resultado Final */
.final-result { background: #2d3748; color: white; padding: 30px; border-radius: 12px; text-align: center; margin-top: 30px; box-shadow: 0 10px 15px rgba(0,0,0,0.1); }
.final-result .label { font-size: 0.9rem; letter-spacing: 1px; opacity: 0.8; margin-bottom: 10px; }
.final-result .value { font-size: 2.5rem; font-weight: 800; }
.final-result .value.positive { color: #48bb78; }
.final-result .value.negative { color: #fc8181; }
.final-result .margem { margin-top: 5px; opacity: 0.7; font-size: 0.9rem; }

.actions { text-align: center; margin-top: 30px; }
.btn-save { background: #38a169; color: white; border: none; padding: 15px 40px; border-radius: 8px; font-size: 1.1rem; font-weight: bold; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.2s; }
.btn-save:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }

/* Histórico */
.historico-box { margin-top: 50px; background: white; border-radius: 8px; border: 1px solid #edf2f7; padding: 20px; }
.hist-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.clear-link { color: #e53e3e; cursor: pointer; font-size: 0.85rem; text-decoration: underline; }
.hist-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #eee; }
.hist-row button { padding: 5px 10px; border: 1px solid #cbd5e0; background: white; border-radius: 4px; cursor: pointer; }

@media (max-width: 600px) {
  .line-row { grid-template-columns: 1fr; gap: 5px; position: relative; padding-bottom: 25px; border-bottom: 1px dashed #eee; margin-bottom: 15px; }
  .btn-del { position: absolute; right: 0; bottom: 0; }
}
</style>