<script setup>
import { ref, computed } from 'vue'
import ModuleLayout from '../../components/ModuleLayout.vue'
import { menuContabilidade } from '../../constants/menuContabilidade.js'

// --- Catálogo de Contas (Opções para o Select) ---
const opcoes = {
  ac: ['Caixa e Equivalentes', 'Contas a Receber', 'Estoques', 'Tributos a Recuperar', 'Despesas Antecipadas', 'Outros'],
  anc: ['Realizável a Longo Prazo', 'Investimentos', 'Imobilizado', 'Intangível', 'Depreciação Acumulada'],
  pc: ['Fornecedores', 'Empréstimos e Financiamentos', 'Obrigações Trabalhistas', 'Impostos a Recolher', 'Dividendos a Pagar'],
  pnc: ['Empréstimos Longo Prazo', 'Provisões', 'Impostos Diferidos', 'Partes Relacionadas'],
  pl: ['Capital Social', 'Reservas de Lucro', 'Reservas de Capital', 'Ajustes de Avaliação', 'Lucros/Prejuízos Acumulados']
}

// --- Estado dos Dados (A "Planilha") ---
const balanco = ref({
  ativo_circulante: [{ id: 1, conta: 'Caixa e Equivalentes', valor: 0, custom: false }],
  ativo_nao_circulante: [{ id: 1, conta: 'Imobilizado', valor: 0, custom: false }],
  
  passivo_circulante: [{ id: 1, conta: 'Fornecedores', valor: 0, custom: false }],
  passivo_nao_circulante: [{ id: 1, conta: 'Empréstimos Longo Prazo', valor: 0, custom: false }],
  patrimonio_liquido: [{ id: 1, conta: 'Capital Social', valor: 0, custom: false }]
})

// --- Funções de Manipulação da Tabela ---
const adicionarLinha = (grupo) => {
  balanco.value[grupo].push({ 
    id: Date.now(), 
    conta: '', 
    valor: 0,
    custom: false 
  })
}

const removerLinha = (grupo, index) => {
  balanco.value[grupo].splice(index, 1)
}

// Verifica se o usuário escolheu "Outros" ou quer digitar um nome personalizado
const verificarCustom = (linha) => {
  if (linha.conta === 'Outros' || linha.conta === 'Personalizado') {
    linha.custom = true
    linha.conta = '' // Limpa para a pessoa digitar
  }
}

// --- Cálculos Automáticos (Computed) ---
const totalAC = computed(() => balanco.value.ativo_circulante.reduce((acc, item) => acc + item.valor, 0))
const totalANC = computed(() => balanco.value.ativo_nao_circulante.reduce((acc, item) => acc + item.valor, 0))
const totalAtivo = computed(() => totalAC.value + totalANC.value)

const totalPC = computed(() => balanco.value.passivo_circulante.reduce((acc, item) => acc + item.valor, 0))
const totalPNC = computed(() => balanco.value.passivo_nao_circulante.reduce((acc, item) => acc + item.valor, 0))
const totalPL = computed(() => balanco.value.patrimonio_liquido.reduce((acc, item) => acc + item.valor, 0))
const totalPassivoPL = computed(() => totalPC.value + totalPNC.value + totalPL.value)

const diferenca = computed(() => totalAtivo.value - totalPassivoPL.value)

// --- Envio para Backend (Futuro) ---
const salvarBalanco = () => {
  if (diferenca.value !== 0) {
    alert("O Balanço não está fechando! A diferença deve ser zero.")
    return
  }
  console.log("Enviando JSON para Python/Pandas:", balanco.value)
  alert("Dados prontos para análise! (Backend em breve)")
}
</script>

<template>
  <ModuleLayout titulo="Contabilidade" emoji="💰" :itensMenu="menuContabilidade">
    
    <div class="header-pagina">
      <h2>Editor de Balanço Patrimonial</h2>
      <p>Estruture as contas do ativo e passivo para análise de liquidez e solvência.</p>
    </div>

    <div class="balanco-grid">
      
      <div class="coluna ativo-col">
        <div class="grupo-contas">
          <h3>⚡ Ativo Circulante</h3>
          <div class="tabela-linhas">
            <div v-for="(linha, index) in balanco.ativo_circulante" :key="linha.id" class="linha-input">
              <input v-if="linha.custom" v-model="linha.conta" placeholder="Nome da conta..." class="input-nome" autoFocus />
              <select v-else v-model="linha.conta" @change="verificarCustom(linha)" class="select-nome">
                <option value="" disabled>Selecione...</option>
                <option v-for="op in opcoes.ac" :key="op" :value="op">{{ op }}</option>
                <option value="Personalizado">➕ Adicionar Outro...</option>
              </select>

              <input type="number" v-model.number="linha.valor" class="input-valor" placeholder="0,00" step="0.01">
              <button @click="removerLinha('ativo_circulante', index)" class="btn-remove">×</button>
            </div>
            <button @click="adicionarLinha('ativo_circulante')" class="btn-add">+ Adicionar Conta</button>
          </div>
          <div class="subtotal">Total Circulante: R$ {{ totalAC.toFixed(2) }}</div>
        </div>

        <div class="grupo-contas">
          <h3>🏢 Ativo Não Circulante</h3>
          <div class="tabela-linhas">
            <div v-for="(linha, index) in balanco.ativo_nao_circulante" :key="linha.id" class="linha-input">
              <input v-if="linha.custom" v-model="linha.conta" placeholder="Nome da conta..." class="input-nome" />
              <select v-else v-model="linha.conta" @change="verificarCustom(linha)" class="select-nome">
                <option value="" disabled>Selecione...</option>
                <option v-for="op in opcoes.anc" :key="op" :value="op">{{ op }}</option>
                <option value="Personalizado">➕ Adicionar Outro...</option>
              </select>
              <input type="number" v-model.number="linha.valor" class="input-valor">
              <button @click="removerLinha('ativo_nao_circulante', index)" class="btn-remove">×</button>
            </div>
            <button @click="adicionarLinha('ativo_nao_circulante')" class="btn-add">+ Adicionar Conta</button>
          </div>
          <div class="subtotal">Total Não Circulante: R$ {{ totalANC.toFixed(2) }}</div>
        </div>

        <div class="total-final ativo-bg">
          <span>TOTAL ATIVO</span>
          <strong>R$ {{ totalAtivo.toFixed(2) }}</strong>
        </div>
      </div>

      <div class="coluna passivo-col">
        <div class="grupo-contas">
          <h3>⏳ Passivo Circulante</h3>
          <div class="tabela-linhas">
            <div v-for="(linha, index) in balanco.passivo_circulante" :key="linha.id" class="linha-input">
              <input v-if="linha.custom" v-model="linha.conta" placeholder="Nome da conta..." class="input-nome" />
              <select v-else v-model="linha.conta" @change="verificarCustom(linha)" class="select-nome">
                <option value="" disabled>Selecione...</option>
                <option v-for="op in opcoes.pc" :key="op" :value="op">{{ op }}</option>
                <option value="Personalizado">➕ Adicionar Outro...</option>
              </select>
              <input type="number" v-model.number="linha.valor" class="input-valor">
              <button @click="removerLinha('passivo_circulante', index)" class="btn-remove">×</button>
            </div>
            <button @click="adicionarLinha('passivo_circulante')" class="btn-add">+ Adicionar Conta</button>
          </div>
          <div class="subtotal">Total P. Circulante: R$ {{ totalPC.toFixed(2) }}</div>
        </div>

        <div class="grupo-contas">
          <h3>🗓️ Passivo Não Circulante</h3>
          <div class="tabela-linhas">
            <div v-for="(linha, index) in balanco.passivo_nao_circulante" :key="linha.id" class="linha-input">
              <input v-if="linha.custom" v-model="linha.conta" placeholder="Nome da conta..." class="input-nome" />
              <select v-else v-model="linha.conta" @change="verificarCustom(linha)" class="select-nome">
                <option value="" disabled>Selecione...</option>
                <option v-for="op in opcoes.pnc" :key="op" :value="op">{{ op }}</option>
                <option value="Personalizado">➕ Adicionar Outro...</option>
              </select>
              <input type="number" v-model.number="linha.valor" class="input-valor">
              <button @click="removerLinha('passivo_nao_circulante', index)" class="btn-remove">×</button>
            </div>
            <button @click="adicionarLinha('passivo_nao_circulante')" class="btn-add">+ Adicionar Conta</button>
          </div>
          <div class="subtotal">Total P. Não Circulante: R$ {{ totalPNC.toFixed(2) }}</div>
        </div>

        <div class="grupo-contas destaque-pl">
          <h3>💎 Patrimônio Líquido</h3>
          <div class="tabela-linhas">
            <div v-for="(linha, index) in balanco.patrimonio_liquido" :key="linha.id" class="linha-input">
              <input v-if="linha.custom" v-model="linha.conta" placeholder="Nome da conta..." class="input-nome" />
              <select v-else v-model="linha.conta" @change="verificarCustom(linha)" class="select-nome">
                <option value="" disabled>Selecione...</option>
                <option v-for="op in opcoes.pl" :key="op" :value="op">{{ op }}</option>
                <option value="Personalizado">➕ Adicionar Outro...</option>
              </select>
              <input type="number" v-model.number="linha.valor" class="input-valor">
              <button @click="removerLinha('patrimonio_liquido', index)" class="btn-remove">×</button>
            </div>
            <button @click="adicionarLinha('patrimonio_liquido')" class="btn-add">+ Adicionar Conta</button>
          </div>
          <div class="subtotal">Total PL: R$ {{ totalPL.toFixed(2) }}</div>
        </div>

        <div class="total-final passivo-bg">
          <span>TOTAL PASSIVO + PL</span>
          <strong>R$ {{ totalPassivoPL.toFixed(2) }}</strong>
        </div>
      </div>
    </div>

    <div class="validacao-bar" :class="{ 'erro': diferenca !== 0, 'sucesso': diferenca === 0 }">
      <div class="status">
        <span v-if="diferenca === 0">✅ Balanço Fechado com Sucesso!</span>
        <span v-else>⚠️ O Balanço não fecha! Diferença: <strong>R$ {{ diferenca.toFixed(2) }}</strong></span>
      </div>
      <button class="btn-processar" :disabled="diferenca !== 0" @click="salvarBalanco">
        Processar Indicadores
      </button>
    </div>

  </ModuleLayout>
</template>

<style scoped>
.header-pagina { text-align: center; margin-bottom: 30px; }
.header-pagina h2 { color: #2c3e50; margin-bottom: 5px; }
.header-pagina p { color: #7f8c8d; }

.balanco-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 80px; } /* Espaço pro footer fixo */

/* Estilos de Grupo */
.grupo-contas { background: white; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 20px; }
.destaque-pl { border-color: #3498db; background: #f4faff; }

h3 { margin-top: 0; font-size: 1.1rem; color: #2c3e50; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px; margin-bottom: 15px; }

/* Linhas Dinâmicas */
.tabela-linhas { display: flex; flex-direction: column; gap: 10px; }
.linha-input { display: grid; grid-template-columns: 2fr 1fr 30px; gap: 10px; align-items: center; }

.select-nome, .input-nome { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; background: white; }
.input-valor { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; text-align: right; font-family: monospace; }
.input-valor:focus { border-color: #2c3e50; outline: none; background: #fdfdfd; }

.btn-remove { background: none; border: none; color: #e74c3c; cursor: pointer; font-size: 1.2rem; font-weight: bold; }
.btn-remove:hover { color: #c0392b; background: #ffeaea; border-radius: 4px; }

.btn-add { background: none; border: 1px dashed #ccc; padding: 8px; width: 100%; margin-top: 10px; border-radius: 4px; cursor: pointer; color: #666; font-size: 0.9rem; }
.btn-add:hover { border-color: #2c3e50; color: #2c3e50; background: #f9f9f9; }

/* Subtotais e Totais */
.subtotal { text-align: right; font-size: 0.9rem; color: #666; margin-top: 10px; font-weight: 500; }

.total-final { padding: 20px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; font-size: 1.2rem; margin-top: 10px; }
.ativo-bg { background-color: #e8f5e9; color: #27ae60; border: 1px solid #a5d6a7; }
.passivo-bg { background-color: #ffebee; color: #c0392b; border: 1px solid #ef9a9a; }

/* Barra de Validação Flutuante */
.validacao-bar {
  position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
  width: 90%; max-width: 800px;
  background: #333; color: white;
  padding: 15px 30px;
  border-radius: 50px;
  display: flex; justify-content: space-between; align-items: center;
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
  transition: all 0.3s;
}
.validacao-bar.erro { background: #c0392b; }
.validacao-bar.sucesso { background: #27ae60; }

.btn-processar { 
  background: white; color: #333; border: none; padding: 10px 20px; border-radius: 20px; 
  cursor: pointer; font-weight: bold; transition: 0.2s; 
}
.btn-processar:hover { transform: scale(1.05); }
.btn-processar:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

@media (max-width: 900px) {
  .balanco-grid { grid-template-columns: 1fr; }
  .validacao-bar { flex-direction: column; gap: 10px; border-radius: 12px; bottom: 10px; }
}
</style>