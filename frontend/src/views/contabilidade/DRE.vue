<script setup>
import { ref, computed, onMounted } from 'vue'
import ModuleLayout from '../../components/ModuleLayout.vue'
import DropdownEditable from '../../components/DropdownEditable.vue'
import { menuContabilidade } from '../../constants/menus/menuContabilidade.js'
import { opcoesDRE } from '../../constants/options/contabilidade.js'
import BtnExcel from '../../components/BtnExcel.vue'

// --- Estrutura de Dados (Espelho da Planilha) ---
const dre = ref({
  receita_bruta: [{ id: 1, conta: 'Receita Bruta de Produtos', valor: 0 }],
  deducoes: [{ id: 2, conta: 'Impostos sobre a Receita Bruta', valor: 0 }],
  
  // Custos
  custos_producao: [{ id: 3, conta: 'Pessoal - CTO', valor: 0 }],
  custos_venda: [{ id: 4, conta: 'CPV / CMV', valor: 0 }],
  
  // Despesas Operacionais
  desp_comerciais: [{ id: 5, conta: 'Pessoal - CML', valor: 0 }],
  desp_administrativas: [{ id: 6, conta: 'Pessoal - ADM', valor: 0 }],
  outras_ops: [{ id: 7, conta: 'Outras Despesas Operacionais', valor: 0 }], // Pode ser +/-

  // Financeiro
  financeiro: [{ id: 8, conta: 'Despesas Financeiras', valor: 0 }],
  
  // Impostos
  impostos: [{ id: 9, conta: 'Provisão para IR/CS', valor: 0 }]
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
// Helper que soma sempre usando Math.abs para garantir o comportamento matemático esperado
// (Usuário digita 1000, nós tratamos como custo/despesa dependendo do bloco)
const somar = (lista) => lista.reduce((acc, item) => acc + (Number(item.valor) || 0), 0)

// --- CÁLCULOS (Fórmulas) ---

// 1. Receita Líquida = Receita Bruta - Deduções
const totalReceitaBruta = computed(() => somar(dre.value.receita_bruta))
const totalDeducoes = computed(() => somar(dre.value.deducoes))
const receitaLiquida = computed(() => totalReceitaBruta.value - Math.abs(totalDeducoes.value))

// 2. Lucro Bruto = Rec. Líquida - (Custos Produção + Custos Venda)
const totalCustosProd = computed(() => somar(dre.value.custos_producao))
const totalCustosVenda = computed(() => somar(dre.value.custos_venda))
const lucroBruto = computed(() => receitaLiquida.value - Math.abs(totalCustosProd.value) - Math.abs(totalCustosVenda.value))

// 3. Lucro Operacional = Lucro Bruto - (Comerciais + Adm + Outras)
const totalComerciais = computed(() => somar(dre.value.desp_comerciais))
const totalAdministrativas = computed(() => somar(dre.value.desp_administrativas))
// Outras ops: assumimos que o usuário digita negativo para despesa e positivo para receita
const totalOutrasOps = computed(() => somar(dre.value.outras_ops)) 

const lucroOperacional = computed(() => 
  lucroBruto.value - Math.abs(totalComerciais.value) - Math.abs(totalAdministrativas.value) + totalOutrasOps.value
)

// 4. Lucro Antes IR (LAIR) = Operacional + Financeiro
const totalFinanceiro = computed(() => somar(dre.value.financeiro))
const lucroAntesIR = computed(() => lucroOperacional.value + totalFinanceiro.value)

// 5. Lucro Líquido
const totalImpostos = computed(() => somar(dre.value.impostos))
const lucroLiquido = computed(() => lucroAntesIR.value - Math.abs(totalImpostos.value))

// Margem
const margemLiquida = computed(() => {
  if (totalReceitaBruta.value === 0) return 0
  return ((lucroLiquido.value / totalReceitaBruta.value) * 100).toFixed(1)
})

// --- Ações ---
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
  if(confirm('Carregar esta versão substituirá os dados atuais. Continuar?')) {
    dre.value = JSON.parse(JSON.stringify(item.dados))
  }
}
const limparHistorico = () => {
  if(confirm('Tem certeza? Isso apagará todo o histórico da DRE.')) {
    historico.value = []
    localStorage.removeItem('historico_dre')
  }
}
</script>

<template>
  <ModuleLayout titulo="Contabilidade" emoji="💰" :itensMenu="menuContabilidade">
    
    <div class="header-pagina">
      <h2>DRE Gerencial</h2>
      <p>Estruture a Demonstração do Resultado conforme os grupos abaixo.</p>
    </div>

    <div class="dre-container">
      
      <div class="section-block receita">
        <div class="section-header">
          <h3>(+) Receita Bruta de Produtos</h3>
          <span>R$ {{ totalReceitaBruta.toFixed(2) }}</span>
        </div>
        <div v-for="(item, idx) in dre.receita_bruta" :key="item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.receita" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('receita_bruta', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('receita_bruta')" class="btn-add">+ Adicionar</button>
      </div>

      <div class="section-block deducao">
        <div class="section-header">
          <h3>(-) Deduções sobre a Receita Bruta</h3>
          <span>R$ {{ totalDeducoes.toFixed(2) }}</span>
        </div>
        <div v-for="(item, idx) in dre.deducoes" :key="item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.deducoes" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('deducoes', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('deducoes')" class="btn-add">+ Adicionar</button>
      </div>

      <div class="result-bar">
        <span>= Receita Líquida</span>
        <strong>R$ {{ receitaLiquida.toLocaleString('pt-BR', {minimumFractionDigits: 2}) }}</strong>
      </div>

      <div class="section-block custo">
        <div class="section-header">
          <h3>(-) Custos de Produtos, Mercadorias e Serviços</h3>
          <span>R$ {{ (totalCustosProd + totalCustosVenda).toFixed(2) }}</span>
        </div>
        
        <h4 class="sub-title">Formação dos Custos (CTO)</h4>
        <div v-for="(item, idx) in dre.custos_producao" :key="item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.custos_producao" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('custos_producao', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('custos_producao')" class="btn-add sub-btn">+ Adicionar CTO</button>

        <h4 class="sub-title mt-4">Custos de Venda (CMV/CPV)</h4>
        <div v-for="(item, idx) in dre.custos_venda" :key="'venda'+item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.custos_venda" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('custos_venda', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('custos_venda')" class="btn-add sub-btn">+ Adicionar CMV</button>
      </div>

      <div class="result-bar destaque">
        <span>= Lucro Bruto</span>
        <strong>R$ {{ lucroBruto.toLocaleString('pt-BR', {minimumFractionDigits: 2}) }}</strong>
      </div>

      <div class="section-block despesa">
        <div class="section-header">
          <h3>(-) Despesas Gerais e Administrativas</h3>
          <span>R$ {{ (totalComerciais + totalAdministrativas - totalOutrasOps).toFixed(2) }}</span>
        </div>

        <h4 class="sub-title">Despesas Comerciais (CML)</h4>
        <div v-for="(item, idx) in dre.desp_comerciais" :key="item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.desp_comerciais" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('desp_comerciais', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('desp_comerciais')" class="btn-add sub-btn">+ Adicionar CML</button>

        <h4 class="sub-title mt-4">Despesas Administrativas (ADM)</h4>
        <div v-for="(item, idx) in dre.desp_administrativas" :key="'adm'+item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.desp_administrativas" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('desp_administrativas', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('desp_administrativas')" class="btn-add sub-btn">+ Adicionar ADM</button>

        <h4 class="sub-title mt-4">Outras Receitas/Despesas Operacionais</h4>
        <p class="hint">Positivo para Receita, Negativo para Despesa</p>
        <div v-for="(item, idx) in dre.outras_ops" :key="'out'+item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.outras_ops" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('outras_ops', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('outras_ops')" class="btn-add sub-btn">+ Adicionar Outros</button>
      </div>

      <div class="result-bar">
        <span>= Lucro Operacional</span>
        <strong>R$ {{ lucroOperacional.toLocaleString('pt-BR', {minimumFractionDigits: 2}) }}</strong>
      </div>

      <div class="section-block financeiro">
        <div class="section-header">
          <h3>(+/-) Resultado Financeiro Líquido</h3>
          <span>R$ {{ totalFinanceiro.toFixed(2) }}</span>
        </div>
        <div v-for="(item, idx) in dre.financeiro" :key="item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.financeiro" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('financeiro', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('financeiro')" class="btn-add">+ Adicionar Financeiro</button>
      </div>

      <div class="result-bar">
        <span>= Lucro Antes do IR e CS</span>
        <strong>R$ {{ lucroAntesIR.toLocaleString('pt-BR', {minimumFractionDigits: 2}) }}</strong>
      </div>

      <div class="section-block deducao">
        <div class="section-header">
          <h3>(-) Impostos sobre Lucro</h3>
          <span>R$ {{ totalImpostos.toFixed(2) }}</span>
        </div>
        <div v-for="(item, idx) in dre.impostos" :key="item.id" class="line-row">
          <DropdownEditable v-model="item.conta" :opcoes="opcoesDRE.impostos" />
          <input type="number" v-model.number="item.valor" class="input-valor" placeholder="0.00">
          <button @click="removeLinha('impostos', idx)" class="btn-del">×</button>
        </div>
        <button @click="addLinha('impostos')" class="btn-add">+ Adicionar Imposto</button>
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
        <BtnExcel 
          :dados="dre" 
          tipo="dre" 
          nomeArquivo="DRE_Gerencial.xlsx"
          style="margin-left: 15px;" 
        />
      </div>

      <div class="historico-area">
        <div class="hist-header">
          <h3>Histórico de Versões</h3>
          <button v-if="historico.length > 0" class="btn-limpar-hist" @click="limparHistorico">Limpar Histórico</button>
        </div>
        
        <div v-if="historico.length > 0" class="lista-historico">
          <div v-for="(item, idx) in historico" :key="idx" class="item-hist">
            <div class="info">
              <strong>{{ item.data }}</strong>
              <span>Lucro Líquido: R$ {{ item.lucro.toLocaleString('pt-BR') }} ({{ item.margem }}%)</span>
            </div>
            <button class="btn-carregar" @click="carregarVersao(item)">Carregar</button>
          </div>
        </div>

        <div v-else class="hist-vazio">
          <span class="icon">📂</span>
          <p>Nenhuma DRE salva ainda.</p>
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

/* Blocos */
.section-block { background: white; padding: 20px; border-radius: 8px; border: 1px solid #edf2f7; margin-bottom: 15px; }
.section-header { display: flex; justify-content: space-between; margin-bottom: 15px; font-weight: 600; color: #4a5568; border-bottom: 1px solid #eee; padding-bottom: 10px; }
.receita .section-header { color: #38a169; }
.deducao .section-header, .custo .section-header, .despesa .section-header { color: #e53e3e; }

/* Subtítulos dentro dos blocos */
.sub-title { margin: 10px 0 5px 0; font-size: 0.9rem; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700; }
.mt-4 { margin-top: 20px; border-top: 1px dashed #eee; padding-top: 15px; }

.line-row { display: grid; grid-template-columns: 3fr 1fr 30px; gap: 10px; margin-bottom: 8px; align-items: center; }
.input-valor { padding: 10px; border: 1px solid #e2e8f0; border-radius: 6px; text-align: right; font-family: monospace; font-weight: 600; height: 42px; box-sizing: border-box; }
.input-valor:focus { border-color: #4299e1; outline: none; }

.btn-del { border: none; background: none; color: #cbd5e0; font-size: 1.5rem; cursor: pointer; }
.btn-del:hover { color: #e53e3e; }

.btn-add { background: none; border: 1px dashed #cbd5e0; color: #718096; padding: 8px; width: 100%; border-radius: 6px; cursor: pointer; margin-top: 5px; transition: 0.2s; }
.btn-add:hover { border-color: #4299e1; color: #4299e1; background: #ebf8ff; }
.sub-btn { font-size: 0.85rem; padding: 5px; } /* Botão menor para subgrupos */

.hint { font-size: 0.8rem; color: #a0aec0; margin-top: -5px; margin-bottom: 10px; font-style: italic; }

/* Totais */
.result-bar { background: #f7fafc; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-radius: 8px; margin-bottom: 15px; font-weight: 500; color: #4a5568; border-left: 4px solid #cbd5e0; }
.result-bar.destaque { background: #edf2f7; border-left-color: #2c3e50; font-size: 1.1rem; }

.final-result { background: #2d3748; color: white; padding: 30px; border-radius: 12px; text-align: center; margin-top: 30px; box-shadow: 0 10px 15px rgba(0,0,0,0.1); }
.final-result .label { font-size: 0.9rem; letter-spacing: 1px; opacity: 0.8; margin-bottom: 10px; }
.final-result .value { font-size: 2.5rem; font-weight: 800; }
.final-result .value.positive { color: #48bb78; }
.final-result .value.negative { color: #fc8181; }
.final-result .margem { margin-top: 5px; opacity: 0.7; font-size: 0.9rem; }

.actions { text-align: center; margin-top: 30px; }
.btn-save { background: #38a169; color: white; border: none; padding: 15px 40px; border-radius: 8px; font-size: 1.1rem; font-weight: bold; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.2s; }
.btn-save:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }

/* Histórico (Layout igual ao Balanço) */
.historico-area { max-width: 800px; margin: 50px auto 50px auto; }
.hist-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.hist-header h3 { font-size: 1.2rem; color: #2c3e50; margin: 0; }
.btn-limpar-hist { background: none; border: none; color: #e53e3e; cursor: pointer; text-decoration: underline; font-size: 0.9rem; }

.lista-historico { display: flex; flex-direction: column; gap: 10px; }
.item-hist { background: white; padding: 15px; border-radius: 8px; border: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.item-hist .info strong { display: block; color: #2c3e50; }
.item-hist .info span { color: #666; font-size: 0.9rem; }
.btn-carregar { background: #edf2f7; color: #4a5568; border: 1px solid #cbd5e0; padding: 6px 12px; border-radius: 4px; cursor: pointer; transition: 0.2s; }
.btn-carregar:hover { background: #e2e8f0; border-color: #a0aec0; }

.hist-vazio { text-align: center; padding: 30px; background: #f9f9f9; border-radius: 8px; color: #a0aec0; border: 2px dashed #eee; }
.hist-vazio .icon { font-size: 2rem; display: block; margin-bottom: 10px; opacity: 0.5; }

@media (max-width: 600px) {
  .line-row { grid-template-columns: 1fr; gap: 5px; position: relative; padding-bottom: 25px; border-bottom: 1px dashed #eee; margin-bottom: 15px; }
  .btn-del { position: absolute; right: 0; bottom: 0; }
}
</style>