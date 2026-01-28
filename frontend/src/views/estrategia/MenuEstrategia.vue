<script setup>
import ModuleLayout from '../../components/ModuleLayout.vue'

const menuEstrategia = [
  { nome: 'Visão Geral', link: '/estrategia' },
  { nome: 'Calculadora NPS', link: '/estrategia/nps' },
  { nome: 'Matriz SWOT (Em breve)', link: '#' },
  { nome: 'Análise de Sentimento (IA)', link: '#' }
]
</script>

<template>
  <ModuleLayout 
    titulo="Estratégia" 
    emoji="🎯" 
    :itensMenu="menuEstrategia"
  >
    <div class="welcome-screen">
      <h2>Inteligência de Mercado</h2>
      <p>Monitore a saúde da marca e o posicionamento estratégico.</p>
      
      <div class="stats-resumo">
        <div class="stat-box">
          <span>CAC (Custo Aquisição)</span>
          <strong class="neutro">R$ 45,00</strong>
        </div>
        <div class="stat-box">
          <span>LTV (Lifetime Value)</span>
          <strong class="positivo">R$ 890,00</strong>
        </div>
        <div class="stat-box">
          <span>Churn Rate</span>
          <strong class="negativo">2.4%</strong>
        </div>
      </div>

      <div class="aviso-ia">
        <p>🤖 O módulo de <strong>Análise de Sentimento</strong> conectará com a API do Google Reviews em breve.</p>
      </div>
    </div>
  </ModuleLayout>
</template>

<style scoped>
.welcome-screen { text-align: center; padding-top: 40px; }
.stats-resumo { display: flex; gap: 20px; justify-content: center; margin-top: 40px; flex-wrap: wrap; }

.stat-box { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e0e0e0; min-width: 180px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
.stat-box span { display: block; color: #666; font-size: 0.9rem; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
.stat-box strong { display: block; font-size: 1.8rem; color: #2c3e50; }
.stat-box strong.positivo { color: #27ae60; } /* Verde */
.stat-box strong.neutro { color: #2980b9; } /* Azul */
.stat-box strong.negativo { color: #c0392b; } /* Vermelho */

.aviso-ia { margin-top: 60px; background: #f3e5f5; display: inline-block; padding: 15px 30px; border-radius: 50px; color: #8e44ad; font-size: 0.9rem; border: 1px solid #e1bee7; }
</style>