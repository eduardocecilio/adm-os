<script setup>
import { ref } from 'vue'
import ModuleLayout from '../../components/ModuleLayout.vue'
import { getMenuEstrategia } from '../../constants/menus/menuEstrategia.js'
import { useWorkspace } from '../../composables/useWorkspace'

const { activeWorkspace } = useWorkspace()

// Dados do NPS
const form = ref({
  promotores: 0, // Notas 9 e 10
  neutros: 0,    // Notas 7 e 8
  detratores: 0  // Notas 0 a 6
})

const resultado = ref(null)

function calcularNPS() {
  const total = form.value.promotores + form.value.neutros + form.value.detratores
  
  if (total === 0) {
    alert("Preencha a quantidade de respostas.")
    return
  }

  // Fórmula: %Promotores - %Detratores
  const npsScore = ((form.value.promotores - form.value.detratores) / total) * 100
  
  // Classificação de Zona
  let classificacao = ''
  let corClassificacao = ''

  if (npsScore >= 75) {
    classificacao = 'Zona de Excelência 🏆'
    corClassificacao = '#27ae60'
  } else if (npsScore >= 50) {
    classificacao = 'Zona de Qualidade ✅'
    corClassificacao = '#2980b9'
  } else if (npsScore >= 0) {
    classificacao = 'Zona de Aperfeiçoamento ⚠️'
    corClassificacao = '#f39c12'
  } else {
    classificacao = 'Zona Crítica 🚨'
    corClassificacao = '#c0392b'
  }

  resultado.value = {
    score: npsScore.toFixed(0),
    total: total,
    classificacao,
    corClassificacao
  }
}
</script>

<template>
  <ModuleLayout 
    titulo="Estratégia" 
    emoji="🎯" 
    :itensMenu="getMenuEstrategia(activeWorkspace?.id)"
  >
    <div class="ferramenta-wrapper">
      
      <div class="header-ferramenta">
        <h2>Calculadora NPS</h2>
        <p>Net Promoter Score: A métrica definitiva de lealdade do cliente.</p>
      </div>
      
      <div class="grid-container" :class="{ 'ativo': resultado }">
        
        <div class="card input-area">
          <div class="campo">
            <label>Promotores (Notas 9-10)</label>
            <input type="number" v-model="form.promotores" placeholder="Qtd. de pessoas">
          </div>
          <div class="campo">
            <label>Neutros (Notas 7-8)</label>
            <input type="number" v-model="form.neutros" placeholder="Qtd. de pessoas">
          </div>
          <div class="campo">
            <label>Detratores (Notas 0-6)</label>
            <input type="number" v-model="form.detratores" placeholder="Qtd. de pessoas">
          </div>
          
          <button @click="calcularNPS" class="btn-calcular">Calcular Score</button>
        </div>

        <Transition name="slide">
          <div class="card resultado-area" v-if="resultado">
            <h3>Resultado NPS</h3>
            
            <div class="nps-display" :style="{ color: resultado.corClassificacao }">
              <strong>{{ resultado.score }}</strong>
              <span>Pontos</span>
            </div>
            
            <div class="classificacao-box" :style="{ borderColor: resultado.corClassificacao, color: resultado.corClassificacao }">
              {{ resultado.classificacao }}
            </div>

            <div class="detalhes">
              <div class="linha">
                <span>Total de Respostas</span>
                <span>{{ resultado.total }}</span>
              </div>
            </div>
          </div>
        </Transition>

      </div>
    </div>
  </ModuleLayout>
</template>

<style scoped>
/* Reutilizando estrutura padrão */
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

/* Estilos Específicos do NPS */
.nps-display { text-align: center; margin: 20px 0; }
.nps-display strong { font-size: 4rem; line-height: 1; display: block; }
.nps-display span { font-size: 1rem; text-transform: uppercase; letter-spacing: 2px; opacity: 0.8; }

.classificacao-box { text-align: center; padding: 10px; border: 2px solid; border-radius: 8px; font-weight: bold; margin-bottom: 20px; background: #fafafa; }

.linha { display: flex; justify-content: space-between; margin-top: 20px; padding-top: 10px; border-top: 1px solid #eee; color: #666; }

.slide-enter-active { transition: all 0.8s ease; }
.slide-enter-from { opacity: 0; transform: translateX(30px); }

@media (max-width: 900px) { .grid-container.ativo { grid-template-columns: 1fr; gap: 20px; } }
</style>