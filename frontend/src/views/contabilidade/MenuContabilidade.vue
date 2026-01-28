<script setup>
import ModuleLayout from '../../components/ModuleLayout.vue'

// O Menu reflete a estrutura de Contabilidade Corporativa
const menuContabilidade = [
  { nome: 'Visão Geral', link: '/contabilidade' },
  { nome: 'Cálculo de ROI/ROE', link: '/contabilidade/indicadores' },
  { nome: 'Análise de DRE (Em breve)', link: '#' },
  { nome: 'Balanço Patrimonial (Em breve)', link: '#' }
]
</script>

<template>
  <ModuleLayout 
    titulo="Contabilidade" 
    emoji="💰" 
    :itensMenu="menuContabilidade"
  >
    <div class="welcome-screen">
      <h2>Módulo de Controladoria</h2>
      <p>Central de inteligência contábil e análise de performance empresarial.</p>
      
      <div class="stats-resumo">
        <div class="stat-box">
          <span>Lucro Líquido (YTD)</span>
          <strong class="positivo">R$ 1.2M</strong>
        </div>
        <div class="stat-box">
          <span>Margem Líquda</span>
          <strong class="neutro">18.5%</strong>
        </div>
        <div class="stat-box">
          <span>ROE Projetado</span>
          <strong class="positivo">22%</strong>
        </div>
      </div>

      <div class="aviso-importacao">
        <p>📂 Para análises profundas, em breve você poderá importar arquivos <strong>.OFX</strong> e <strong>.CSV</strong> do seu ERP.</p>
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
.stat-box strong.positivo { color: #27ae60; }
.stat-box strong.neutro { color: #f39c12; }

.aviso-importacao { margin-top: 60px; background: #e8f4fd; display: inline-block; padding: 15px 30px; border-radius: 50px; color: #2980b9; font-size: 0.9rem; }
</style>