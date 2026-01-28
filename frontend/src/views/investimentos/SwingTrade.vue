<script setup>
import { ref } from 'vue'
import ModuleLayout from '../../components/ModuleLayout.vue'
import { menuInvestimentos } from '../../constants/menus/menuInvestimentos.js'

const form = ref({
  preco_compra: 0,
  preco_venda: 0,
  quantidade: 100,
  taxa_corretagem: 2.00
})

const resultado = ref(null)

async function calcularNoBackend() {
  try {
    const resposta = await fetch('http://127.0.0.1:8000/investimentos/swing-trade/calcular', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'x-token': 'admin-os-segredo-2026'
      },
      body: JSON.stringify(form.value)
    })
    const dados = await resposta.json()
    resultado.value = dados 
  } catch (erro) {
    alert("Erro ao conectar com o servidor.")
  }
}
</script>

<template>
  <ModuleLayout 
    titulo="Investimentos" 
    emoji="📈" 
    :itensMenu="menuInvestimentos"
  >
    
    <div class="ferramenta-wrapper">
      <div class="header-ferramenta">
        <h2>Simulador de Swing Trade</h2>
        <p>Calcule o lucro líquido descontando IR (15%) e Taxas da B3.</p>
      </div>
      
      <div class="grid-container" :class="{ 'ativo': resultado }">
         <div class="card input-area">
          <div class="campo">
            <label>Preço de Compra (R$)</label>
            <input type="number" v-model="form.preco_compra" step="0.01">
          </div>
          <div class="campo">
            <label>Preço de Venda (R$)</label>
            <input type="number" v-model="form.preco_venda" step="0.01">
          </div>
          <div class="campo">
            <label>Quantidade</label>
            <input type="number" v-model="form.quantidade">
          </div>
          
          <button @click="calcularNoBackend" class="btn-calcular">Calcular Resultado</button>
        </div>

        <Transition name="slide">
          <div class="card resultado-area" v-if="resultado">
            <h3>Resumo da Operação</h3>
            
            <div class="resumo-item lucro">
              <span>Lucro Líquido</span>
              <strong>R$ {{ resultado.resumo.lucro_liquido }}</strong>
            </div>
            
            <div class="detalhes">
              <div class="linha">
                <span>Imposto de Renda</span>
                <span>R$ {{ resultado.resumo.imposto_renda }}</span>
              </div>
              <div class="linha">
                <span>Custos Totais</span>
                <span>R$ {{ resultado.resumo.custos_totais }}</span>
              </div>
              <div class="linha destaque-bruto">
                <span>Lucro Bruto</span>
                <span>R$ {{ resultado.resumo.lucro_bruto }}</span>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>

  </ModuleLayout>
</template>

<style scoped>
/* Wrapper Global */
.ferramenta-wrapper { padding: 0 20px; }

/* Cabeçalho - Agora fixo e sempre centralizado */
.header-ferramenta { 
  text-align: center; 
  margin-bottom: 40px; 
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}
.header-ferramenta h2 { margin: 0; color: #2c3e50; font-size: 2rem; }
.header-ferramenta p { color: #666; margin-top: 8px; font-size: 1.1rem; }

/* --- GRID SYSTEM --- */
.grid-container {
  display: grid;
  grid-template-columns: 1fr; 
  gap: 0; 
  max-width: 450px; 
  margin: 0 auto;
  transition: all 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* Estado ATIVO (Com Resultado): Expande para 2 Colunas */
.grid-container.ativo {
  grid-template-columns: 1fr 1fr;
  gap: 40px; 
  max-width: 1000px;
}

/* Cards */
.card { 
  background: white; 
  padding: 30px; 
  border-radius: 12px; 
  border: 1px solid #e0e0e0;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  height: fit-content;
}

/* Inputs */
.campo { margin-bottom: 15px; }
label { display: block; margin-bottom: 5px; font-weight: 600; color: #2c3e50; }
input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; box-sizing: border-box; }
input:focus { border-color: #42b983; outline: none; }

/* Botão Calcular */
.btn-calcular { width: 100%; background: #2c3e50; color: white; padding: 12px; border: none; border-radius: 6px; font-size: 1rem; cursor: pointer; font-weight: bold; margin-top: 10px; transition: 0.2s; }
.btn-calcular:hover { background: #42b983; }

/* Resultados */
.resumo-item { text-align: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #eee; }
.lucro strong { color: #27ae60; font-size: 2.2rem; display: block; margin-top: 5px; }
.linha { display: flex; justify-content: space-between; margin-bottom: 10px; color: #555; }
.destaque-bruto { font-weight: 600; color: #2c3e50; margin-top: 15px; padding-top: 15px; border-top: 1px dashed #ddd; }

/* Animação de Entrada do Card Resultado */
.slide-enter-active { transition: all 0.8s ease; }
.slide-enter-from { opacity: 0; transform: translateX(30px); }
.slide-leave-to { opacity: 0; }

/* Responsividade Celular */
@media (max-width: 900px) {
  .grid-container.ativo { grid-template-columns: 1fr; gap: 20px; }
}
</style>