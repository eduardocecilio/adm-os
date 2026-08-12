<script setup>
import { useRouter } from 'vue-router'
import Header from '../components/Header.vue'
import { useWorkspace } from '../composables/useWorkspace'

const router = useRouter()
const { activeWorkspace } = useWorkspace()
</script>

<template>
  <div class="dashboard-page">
    <Header />

    <div class="dashboard-content" v-if="activeWorkspace">
      <header class="page-title">
        <h1>Bem-vindo ao AdmOS</h1>
        <p class="subtitle">Sistema de Inteligência Corporativa — {{ activeWorkspace.name }}</p>
      </header>

      <div class="grid">

        <div class="card" @click="router.push(`/${activeWorkspace.id}/contabilidade`)">
          <div class="icon">💰</div>
          <h3>Contabilidade</h3>
          <p>Análise de Balanços, Liquidez e DRE.</p>
        </div>

        <div class="card" @click="router.push(`/${activeWorkspace.id}/investimentos`)">
          <div class="icon">📈</div>
          <h3>Investimentos</h3>
          <p>Análise de mercado, Risco e Estratégias.</p>
        </div>

        <div class="card" @click="router.push(`/${activeWorkspace.id}/estrategia`)">
          <div class="icon">🎯</div>
          <h3>Estratégia</h3>
          <p>Análise de sentimento, NPS e KPIs de marca.</p>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-content { max-width: 1200px; margin: 0 auto; padding: 0 20px; text-align: center; }
.page-title { margin-bottom: 40px; }
.subtitle { color: #666; margin-top: 10px; font-size: 1.2rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; padding-bottom: 40px; }
.card {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e0e0e0;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  text-align: left;
}
.card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px rgba(0,0,0,0.1); border-color: #42b983; }
.icon { font-size: 2.5rem; margin-bottom: 15px; }
h3 { color: #2c3e50; margin: 0 0 10px 0; font-size: 1.5rem; }
p { color: #666; line-height: 1.5; }
</style>