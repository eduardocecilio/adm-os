<script setup>
import { ref } from 'vue'
import ModuleLayout from '../../components/ModuleLayout.vue'
import { menuContabilidade } from '../../constants/menuContabilidade.js'

// Dados do Formulário
const form = ref({
  lucroLiquido: 0,
  patrimonioLiquido: 0,
  investimentoInicial: 0
})

const resultado = ref(null)

// Cálculo Simples no Front (depois passamos pro Python)
function calcularIndicadores() {
  if (form.value.patrimonioLiquido <= 0 || form.value.investimentoInicial <= 0) {
    alert("Preencha valores maiores que zero.")
    return
  }

  // ROE = (Lucro Líquido / Patrimônio Líquido) * 100
  const roe = (form.value.lucroLiquido / form.value.patrimonioLiquido) * 100
  
  // ROI = ((Lucro Líquido - Investimento) / Investimento) * 100 
  // *Simplificado para exemplo
  const roi = (form.value.lucroLiquido / form.value.investimentoInicial) * 100

  resultado.value = {
    roe: roe.toFixed(2),
    roi: roi.toFixed(2)
  }
}
</script>

<template>
  <ModuleLayout 
    titulo="Contabilidade" 
    emoji="💰" 
    :itensMenu="menuContabilidade"
  >
    <div class="ferramenta-wrapper">
      
      <div class="header-ferramenta">
        <h2>Indicadores de Performance</h2>
        <p>Calcule a eficiência do capital (ROE) e o retorno sobre investimento (ROI).</p>
      </div>
      
      <div class="grid-container" :class="{ 'ativo': resultado }">
        
        <div class="card input-area">
          <div class="campo">
            <label>Lucro Líquido (R$)</label>
            <input type="number" v-model="form.lucroLiquido">
          </div>
          <div class="campo">
            <label>Patrimônio Líquido (R$)</label>
            <input type="number" v-model="form.patrimonioLiquido">
          </div>
          <div class="campo">
            <label>Investimento Inicial (R$)</label>
            <input type="number" v-model="form.investimentoInicial">
          </div>
          
          <button @click="calcularIndicadores" class="btn-calcular">Calcular KPIs</button>
        </div>

        <Transition name="slide">
          <div class="card resultado-area" v-if="resultado">
            <h3>Resultado da Análise</h3>
            
            <div class="kpi-grid">
              <div class="kpi-box">
                <span>ROE (Retorno s/ Patrimônio)</span>
                <strong>{{ resultado.roe }}%</strong>
                <small>Eficiência dos Acionistas</small>
              </div>
              
              <div class="kpi-box">
                <span>ROI (Retorno s/ Investimento)</span>
                <strong>{{ resultado.roi }}%</strong>
                <small>Eficiência do Projeto</small>
              </div>
            </div>
            
            <div class="analise-texto">
              <p v-if="resultado.roe > 15">🚀 <strong>Excelente!</strong> O ROE está acima da média de mercado (15%).</p>
              <p v-else>⚠️ <strong>Atenção:</strong> O retorno está abaixo do ideal para o risco.</p>
            </div>

          </div>
        </Transition>

      </div>
    </div>
  </ModuleLayout>
</template>

<style scoped>
/* Reutilizando a estrutura CSS "Grid Expansivo" do Carteira */
.ferramenta-wrapper { padding: 0 20px; }
.header-ferramenta { text-align: center; margin-bottom: 40px; max-width: 800px; margin-left: auto; margin-right: auto; }
.header-ferramenta h2 { margin: 0; color: #2c3e50; font-size: 2rem; }
.header-ferramenta p { color: #666; margin-top: 8px; }

.grid-container { display: grid; grid-template-columns: 1fr; gap: 0; max-width: 450px; margin: 0 auto; transition: all 0.6s cubic-bezier(0.25, 0.8, 0.25, 1); }
.grid-container.ativo { grid-template-columns: 1fr 1fr; gap: 40px; max-width: 1000px; }

.card { background: white; padding: 30px; border-radius: 12px; border: 1px solid #e0e0e0; height: fit-content; }
.campo { margin-bottom: 15px; }
label { display: block; margin-bottom: 5px; font-weight: 600; color: #2c3e50; }
input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; box-sizing: border-box; }
input:focus { border-color: #42b983; outline: none; }
.btn-calcular { width: 100%; background: #2c3e50; color: white; padding: 12px; border: none; border-radius: 6px; font-size: 1rem; cursor: pointer; font-weight: bold; margin-top: 10px; }
.btn-calcular:hover { background: #42b983; }

/* Estilo Específico dos KPIs */
.kpi-grid { display: flex; gap: 20px; margin-bottom: 20px; }
.kpi-box { flex: 1; background: #f9f9f9; padding: 15px; border-radius: 8px; text-align: center; }
.kpi-box span { display: block; font-size: 0.8rem; color: #666; margin-bottom: 5px; }
.kpi-box strong { display: block; font-size: 1.8rem; color: #2c3e50; }
.kpi-box small { display: block; font-size: 0.7rem; color: #999; margin-top: 5px; }
.analise-texto { border-top: 1px solid #eee; padding-top: 15px; color: #555; }

.slide-enter-active { transition: all 0.8s ease; }
.slide-enter-from { opacity: 0; transform: translateX(30px); }

@media (max-width: 900px) { .grid-container.ativo { grid-template-columns: 1fr; gap: 20px; } }
</style>