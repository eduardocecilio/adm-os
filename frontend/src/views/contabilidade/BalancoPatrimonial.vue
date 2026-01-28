<script setup>
import { ref, computed, onMounted } from 'vue'
import ModuleLayout from '../../components/ModuleLayout.vue'

// --- CORREÇÃO 1: Importar o arquivo .vue direto (sem /index.js) ---
import DropdownEditable from '../../components/DropdownEditable.vue' 

// --- CORREÇÃO 2: Adicionar a pasta 'menus' no caminho ---
import { menuContabilidade } from '../../constants/menus/menuContabilidade.js'

import { opcoesBalanco } from '../../constants/options/contabilidade.js'

// --- Estado dos Dados ---
const balanco = ref({
  ativo_circulante: [{ id: 1, conta: 'Caixa e Equivalentes', valor: 0 }],
  ativo_nao_circulante: [{ id: 2, conta: 'Imobilizado', valor: 0 }],
  passivo_circulante: [{ id: 3, conta: 'Fornecedores', valor: 0 }],
  passivo_nao_circulante: [{ id: 4, conta: 'Empréstimos Longo Prazo', valor: 0 }],
  patrimonio_liquido: [{ id: 5, conta: 'Capital Social', valor: 0 }]
})

const historico = ref([])

onMounted(() => {
  carregarHistoricoLocal()
})

// --- Funções de Tabela ---
const adicionarLinha = (grupo) => {
  balanco.value[grupo].push({ id: Date.now(), conta: '', valor: 0 })
}

const removerLinha = (grupo, index) => {
  balanco.value[grupo].splice(index, 1)
}

// --- Cálculos ---
const somar = (lista) => lista.reduce((acc, item) => acc + (Number(item.valor) || 0), 0)

const totalAC = computed(() => somar(balanco.value.ativo_circulante))
const totalANC = computed(() => somar(balanco.value.ativo_nao_circulante))
const totalAtivo = computed(() => totalAC.value + totalANC.value)

const totalPC = computed(() => somar(balanco.value.passivo_circulante))
const totalPNC = computed(() => somar(balanco.value.passivo_nao_circulante))
const totalPL = computed(() => somar(balanco.value.patrimonio_liquido))
const totalPassivoPL = computed(() => totalPC.value + totalPNC.value + totalPL.value)

const diferenca = computed(() => totalAtivo.value - totalPassivoPL.value)

// --- Persistência ---
const carregarHistoricoLocal = () => {
  const saved = localStorage.getItem('historico_balanco')
  if (saved) historico.value = JSON.parse(saved)
}

const carregarVersao = (versao) => {
  if(confirm('Carregar esta versão substituirá os dados atuais. Continuar?')) {
    balanco.value = JSON.parse(JSON.stringify(versao.dados))
  }
}

const apagarHistorico = () => {
  if(confirm('Limpar todo o histórico?')) {
    historico.value = []
    localStorage.removeItem('historico_balanco')
  }
}

const checarESalvar = () => {
  const dif = diferenca.value
  if (Math.abs(dif) > 0.01) {
    let msg = `⚠️ ERRO: Diferença de R$ ${dif.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
    alert(msg)
    return
  }
  const novo = { data: new Date().toLocaleString('pt-BR'), total: totalAtivo.value, dados: JSON.parse(JSON.stringify(balanco.value)) }
  historico.value.unshift(novo)
  localStorage.setItem('historico_balanco', JSON.stringify(historico.value))
  alert("✅ Balanço salvo no histórico!")
}
</script>

<template>
  <ModuleLayout titulo="Contabilidade" emoji="💰" :itensMenu="menuContabilidade">
    
    <div class="header-pagina">
      <h2>Editor de Balanço Patrimonial</h2>
      <p>Estruture as contas. O Ativo deve ser igual ao Passivo + PL.</p>
    </div>

    <div class="balanco-grid">
      
      <div class="coluna">
        
        <div class="grupo-contas">
          <div class="grupo-header">
            <h3>⚡ Ativo Circulante</h3>
            <span class="badge-total">R$ {{ totalAC.toFixed(2) }}</span>
          </div>
          <div class="tabela-linhas">
            <div v-for="(linha, index) in balanco.ativo_circulante" :key="linha.id" class="linha-input">
              <DropdownEditable v-model="linha.conta" :opcoes="opcoesBalanco.ac" />
              <input type="number" v-model.number="linha.valor" class="input-valor" placeholder="0.00">
              <button @click="removerLinha('ativo_circulante', index)" class="btn-remove">×</button>
            </div>
            <button @click="adicionarLinha('ativo_circulante')" class="btn-add">+ Adicionar</button>
          </div>
        </div>

        <div class="grupo-contas">
          <div class="grupo-header">
            <h3>🏢 Ativo Não Circulante</h3>
            <span class="badge-total">R$ {{ totalANC.toFixed(2) }}</span>
          </div>
          <div class="tabela-linhas">
            <div v-for="(linha, index) in balanco.ativo_nao_circulante" :key="linha.id" class="linha-input">
              <DropdownEditable v-model="linha.conta" :opcoes="opcoesBalanco.anc" />
              <input type="number" v-model.number="linha.valor" class="input-valor">
              <button @click="removerLinha('ativo_nao_circulante', index)" class="btn-remove">×</button>
            </div>
            <button @click="adicionarLinha('ativo_nao_circulante')" class="btn-add">+ Adicionar</button>
          </div>
        </div>

        <div class="card-total ativo-bg">
          <div class="label">TOTAL ATIVO</div>
          <div class="valor">R$ {{ totalAtivo.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) }}</div>
        </div>
      </div>

      <div class="coluna">
        
        <div class="grupo-contas">
          <div class="grupo-header">
            <h3>⏳ Passivo Circulante</h3>
            <span class="badge-total">R$ {{ totalPC.toFixed(2) }}</span>
          </div>
          <div class="tabela-linhas">
            <div v-for="(linha, index) in balanco.passivo_circulante" :key="linha.id" class="linha-input">
              <DropdownEditable v-model="linha.conta" :opcoes="opcoesBalanco.pc" />
              <input type="number" v-model.number="linha.valor" class="input-valor">
              <button @click="removerLinha('passivo_circulante', index)" class="btn-remove">×</button>
            </div>
            <button @click="adicionarLinha('passivo_circulante')" class="btn-add">+ Adicionar</button>
          </div>
        </div>

        <div class="grupo-contas">
          <div class="grupo-header">
            <h3>🗓️ Passivo Não Circulante</h3>
            <span class="badge-total">R$ {{ totalPNC.toFixed(2) }}</span>
          </div>
          <div class="tabela-linhas">
            <div v-for="(linha, index) in balanco.passivo_nao_circulante" :key="linha.id" class="linha-input">
              <DropdownEditable v-model="linha.conta" :opcoes="opcoesBalanco.pnc" />
              <input type="number" v-model.number="linha.valor" class="input-valor">
              <button @click="removerLinha('passivo_nao_circulante', index)" class="btn-remove">×</button>
            </div>
            <button @click="adicionarLinha('passivo_nao_circulante')" class="btn-add">+ Adicionar</button>
          </div>
        </div>

        <div class="grupo-contas destaque-pl">
          <div class="grupo-header">
            <h3>💎 Patrimônio Líquido</h3>
            <span class="badge-total">R$ {{ totalPL.toFixed(2) }}</span>
          </div>
          <div class="tabela-linhas">
            <div v-for="(linha, index) in balanco.patrimonio_liquido" :key="linha.id" class="linha-input">
              <DropdownEditable v-model="linha.conta" :opcoes="opcoesBalanco.pl" />
              <input type="number" v-model.number="linha.valor" class="input-valor">
              <button @click="removerLinha('patrimonio_liquido', index)" class="btn-remove">×</button>
            </div>
            <button @click="adicionarLinha('patrimonio_liquido')" class="btn-add">+ Adicionar</button>
          </div>
        </div>

        <div class="card-total passivo-bg">
          <div class="label">TOTAL PASSIVO + PL</div>
          <div class="valor">R$ {{ totalPassivoPL.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) }}</div>
        </div>
      </div>
    </div>

    <div class="footer-actions">
      <button class="btn-salvar" @click="checarESalvar">
        💾 Salvar Balanço
      </button>
    </div>

    <div class="historico-area" v-if="historico.length > 0">
      <div class="hist-header">
        <h3>Histórico de Versões</h3>
        <button class="btn-limpar-hist" @click="apagarHistorico">Limpar Histórico</button>
      </div>
      <div class="lista-historico">
        <div v-for="(item, idx) in historico" :key="idx" class="item-hist">
          <div class="info">
            <strong>{{ item.data }}</strong>
            <span>Total Ativo: R$ {{ item.total.toLocaleString('pt-BR') }}</span>
          </div>
          <button class="btn-carregar" @click="carregarVersao(item)">Carregar</button>
        </div>
      </div>
    </div>

  </ModuleLayout>
</template>

<style scoped>
.header-pagina { text-align: center; margin-bottom: 30px; }
.header-pagina h2 { color: #2c3e50; margin-bottom: 5px; }
.header-pagina p { color: #7f8c8d; }

.balanco-grid { display: flex; gap: 30px; align-items: stretch; }
.coluna { flex: 1; display: flex; flex-direction: column; }

.grupo-contas { background: white; padding: 20px; border-radius: 12px; border: 1px solid #edf2f7; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 20px; }
.grupo-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #edf2f7; padding-bottom: 12px; margin-bottom: 15px; }
.grupo-header h3 { margin: 0; font-size: 1rem; color: #4a5568; font-weight: 600; }
.badge-total { background: #f7fafc; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; color: #718096; font-weight: bold; }
.destaque-pl { border: 1px solid #bee3f8; background: #ebf8ff; }

.tabela-linhas { display: flex; flex-direction: column; gap: 8px; }
.linha-input { display: grid; grid-template-columns: 60% 1fr 30px; gap: 10px; align-items: center; }

/* INPUT DE VALOR */
.input-valor { width: 100%; padding: 10px; border: 1px solid #e2e8f0; border-radius: 6px; text-align: right; font-family: 'Courier New', monospace; font-weight: 600; box-sizing: border-box; }
.input-valor:focus { border-color: #48bb78; outline: none; }

.btn-remove { background: none; border: none; color: #cbd5e0; cursor: pointer; font-size: 1.4rem; transition: 0.2s; }
.btn-remove:hover { color: #e53e3e; }
.btn-add { background: none; border: 1px dashed #cbd5e0; color: #718096; padding: 8px; width: 100%; margin-top: 5px; border-radius: 6px; font-size: 0.9rem; cursor: pointer; transition: 0.2s; }
.btn-add:hover { border-color: #4299e1; color: #4299e1; background: #ebf8ff; }

.card-total { padding: 20px; border-radius: 12px; text-align: center; margin-top: auto; }
.card-total .label { font-size: 0.85rem; letter-spacing: 1px; margin-bottom: 5px; opacity: 0.8; font-weight: 600; }
.card-total .valor { font-size: 1.8rem; font-weight: 700; }
.ativo-bg { background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); color: white; box-shadow: 0 4px 6px rgba(72, 187, 120, 0.3); }
.passivo-bg { background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%); color: white; box-shadow: 0 4px 6px rgba(229, 62, 62, 0.3); }

.footer-actions { margin-top: 40px; text-align: center; padding-bottom: 20px; border-bottom: 1px solid #eee; margin-bottom: 40px; }
.btn-salvar { background: #2c3e50; color: white; border: none; padding: 15px 40px; font-size: 1.1rem; border-radius: 8px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 6px rgba(44, 62, 80, 0.2); transition: 0.2s; }
.btn-salvar:hover { background: #34495e; transform: translateY(-2px); box-shadow: 0 6px 12px rgba(44, 62, 80, 0.3); }

.historico-area { max-width: 800px; margin: 0 auto 50px auto; }
.hist-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.item-hist { background: white; padding: 15px; border-radius: 8px; border: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;}
.btn-carregar { background: #edf2f7; color: #4a5568; border: 1px solid #cbd5e0; padding: 6px 12px; border-radius: 4px; cursor: pointer; transition: 0.2s; }
.btn-limpar-hist { background: none; border: none; color: #e53e3e; cursor: pointer; text-decoration: underline; }

@media (max-width: 900px) {
  .balanco-grid { flex-direction: column; }
  .coluna { width: 100%; }
}
</style>