<script setup>
import ModuleLayout from '../../components/ModuleLayout.vue'
import { getMenuContabilidade } from '../../constants/menus/menuContabilidade.js'
import { useRouter } from 'vue-router'
import { useWorkspace } from '../../composables/useWorkspace'

const router = useRouter()
const { activeWorkspace } = useWorkspace()

const navegarPara = (rota) => {
  router.push(rota)
}
</script>

<template>
  <ModuleLayout
    titulo="Contabilidade"
    emoji="📊"
    :itensMenu="getMenuContabilidade(activeWorkspace?.id)"
  >
    <div class="dashboard-home">

      <div class="hero-section">
        <h2>Controladoria & Performance</h2>
        <p>Siga o fluxo abaixo para gerar os relatórios de inteligência financeira.</p>
      </div>

      <div class="steps-container">

        <div class="step-card" @click="navegarPara(`/${activeWorkspace?.id}/contabilidade/balanco`)">
          <div class="step-icon">1️⃣</div>
          <h3>Balanço Patrimonial</h3>
          <p>Cadastre os saldos de Ativos e Passivos.</p>
          <div class="tags-importantes">
            <span class="tag">Disponível</span>
            <span class="tag">Estoques</span>
            <span class="tag">Fornecedores</span>
            <span class="tag">Empréstimos</span>
          </div>
        </div>

        <div class="step-card" @click="navegarPara(`/${activeWorkspace?.id}/contabilidade/dre`)">
          <div class="step-icon">2️⃣</div>
          <h3>DRE Gerencial</h3>
          <p>Estruture Receitas, Custos e Despesas.</p>
          <div class="tags-importantes">
            <span class="tag">Receita Bruta</span>
            <span class="tag">CMV / CPV</span>
            <span class="tag">Serviços (3º)</span>
            <span class="tag">Impostos</span>
          </div>
        </div>

        <div class="step-card highlight" @click="navegarPara(`/${activeWorkspace?.id}/contabilidade/indicadores`)">
          <div class="step-icon">3️⃣</div>
          <h3>Indicadores</h3>
          <p>Gere ROI, ROE, Ciclos e Liquidez automaticamente.</p>
          <button class="btn-action">Ver Dashboard ➔</button>
        </div>

      </div>

      <div class="info-guide">
        <h3>⚠️ Guia de Preenchimento para Fórmulas</h3>
        <p>Para que os cálculos funcionem corretamente, certifique-se de preencher ou selecionar os campos marcados com <strong>(*)</strong> nos formulários:</p>

        <div class="guide-grid">
          <div class="guide-item">
            <h4>Para Liquidez</h4>
            <ul>
              <li><strong>Disponível:</strong> Essencial para Liquidez Imediata.</li>
              <li><strong>Estoques:</strong> Essencial para Liquidez Seca.</li>
              <li><strong>Despesas Antecipadas:</strong> Abatido na Liquidez Seca.</li>
            </ul>
          </div>

          <div class="guide-item">
            <h4>Para Rentabilidade (ROI/ROE)</h4>
            <ul>
              <li><strong>Empréstimos (CP e LP):</strong> Usado para calcular o Investimento total.</li>
              <li><strong>Patrimônio Líquido:</strong> Base para o ROE.</li>
              <li><strong>Lucro Líquido (DRE):</strong> O resultado final da operação.</li>
            </ul>
          </div>

          <div class="guide-item">
            <h4>Para Atividade (Ciclos)</h4>
            <ul>
              <li><strong>Fornecedores:</strong> Base para Prazo Médio de Pagamento.</li>
              <li><strong>Contas a Receber:</strong> Base para Prazo Médio de Recebimento.</li>
              <li><strong>Serviços de Terceiros:</strong> Somados ao CMV para calcular as "Compras".</li>
            </ul>
          </div>
        </div>
      </div>

    </div>
  </ModuleLayout>
</template>

<style scoped>
.dashboard-home { padding: 20px; max-width: 1000px; margin: 0 auto; }

.hero-section { text-align: center; margin-bottom: 40px; }
.hero-section h2 { color: #2c3e50; font-size: 2rem; margin-bottom: 10px; }
.hero-section p { color: #7f8c8d; font-size: 1.1rem; }

/* STEPS */
.steps-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; margin-bottom: 50px; }

.step-card {
  background: white; padding: 25px; border-radius: 12px; border: 1px solid #e0e0e0;
  cursor: pointer; transition: all 0.3s ease; position: relative; overflow: hidden;
  display: flex; flex-direction: column;
}
.step-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); border-color: #3498db; }

.step-icon { font-size: 2.5rem; margin-bottom: 15px; }
.step-card h3 { margin: 0 0 10px 0; color: #2c3e50; }
.step-card p { color: #666; font-size: 0.95rem; margin-bottom: 20px; flex-grow: 1; }

.step-card.highlight { background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); color: white; border: none; }
.step-card.highlight h3, .step-card.highlight p { color: white; }
.btn-action { margin-top: auto; background: #27ae60; color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; }

/* TAGS */
.tags-importantes { display: flex; flex-wrap: wrap; gap: 8px; }
.tag { background: #f0f4f8; color: #576574; font-size: 0.75rem; padding: 4px 8px; border-radius: 4px; font-weight: 600; }
.step-card:hover .tag { background: #dfe6e9; color: #2d3436; }

/* GUIA DE INFORMAÇÕES */
.info-guide { background: #f8f9fa; padding: 30px; border-radius: 12px; border-left: 5px solid #f39c12; }
.info-guide h3 { margin-top: 0; color: #e67e22; margin-bottom: 10px; }
.info-guide > p { color: #7f8c8d; margin-bottom: 25px; }

.guide-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; }
.guide-item h4 { color: #2c3e50; border-bottom: 1px solid #e0e0e0; padding-bottom: 8px; margin-bottom: 10px; }
.guide-item ul { padding-left: 20px; margin: 0; }
.guide-item li { margin-bottom: 8px; color: #555; font-size: 0.9rem; line-height: 1.4; }
.guide-item strong { color: #2980b9; }

@media (max-width: 768px) {
  .steps-container, .guide-grid { grid-template-columns: 1fr; }
}
</style>