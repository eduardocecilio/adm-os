<script setup>
import { ref, onMounted } from 'vue'
import ModuleLayout from '../../components/ModuleLayout.vue'
import { menuInvestimentos } from '../../constants/menuInvestimentos.js'

const selic = ref('Carregando...')
const dolar = ref('Carregando...')

onMounted(async () => {
  try {
    const respDolar = await fetch('https://economia.awesomeapi.com.br/last/USD-BRL')
    const dadosDolar = await respDolar.json()
    dolar.value = 'R$ ' + parseFloat(dadosDolar.USDBRL.bid).toFixed(2).replace('.', ',')

    const respSelic = await fetch('https://brasilapi.com.br/api/taxas/v1/selic')
    const dadosSelic = await respSelic.json()
    selic.value = dadosSelic.valor + '%'
  } catch (error) {
    selic.value = 'Erro'
    dolar.value = 'Erro'
  }
})
</script>

<template>
  <ModuleLayout 
    titulo="Investimentos" 
    emoji="📈" 
    :itensMenu="menuInvestimentos"
  >
    <div class="welcome-screen">
      <h2>Mesa de Operações</h2>
      <p>Análise de mercado, gestão de risco e estratégias estruturadas.</p>
      
      <div class="stats-resumo">
        <div class="stat-box">
          <span>Taxa Selic</span>
          <strong :class="{ loading: selic === 'Carregando...' }">{{ selic }}</strong>
        </div>
        <div class="stat-box">
          <span>Dólar PTAX</span>
          <strong :class="{ loading: dolar === 'Carregando...' }">{{ dolar }}</strong>
        </div>
      </div>
    </div>
  </ModuleLayout>
</template>

<style scoped>
.welcome-screen { text-align: center; padding-top: 50px; }
.stats-resumo { display: flex; gap: 20px; justify-content: center; margin-top: 40px; flex-wrap: wrap; }
.stat-box { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e0e0e0; min-width: 180px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
.stat-box span { display: block; color: #666; font-size: 0.9rem; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
.stat-box strong { display: block; font-size: 1.8rem; color: #2c3e50; }
.stat-box strong.loading { font-size: 1rem; color: #999; margin-top: 10px; }
</style>