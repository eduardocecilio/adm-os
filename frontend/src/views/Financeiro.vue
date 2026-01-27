<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <div class="page">
    <header>
      <button @click="router.push('/')" class="back-btn">← Voltar</button>
      <h1>Contabilidade</h1>
    </header>
    
    <div class="content">
      <div class="placeholder-card">
        <span class="icon-big">💰</span>
        <h2>Módulo em Desenvolvimento</h2>
        <p>Em breve você poderá importar arquivos de Balanço Patrimonial e DRE para análise automática.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page { padding: 40px; max-width: 1000px; margin: 0 auto; }
header { display: flex; align-items: center; gap: 20px; margin-bottom: 40px; }
.back-btn { background: white; border: 1px solid #ccc; padding: 8px 16px; border-radius: 6px; cursor: pointer; color: #555; }
.back-btn:hover { background: #eee; }
.content { background: white; padding: 60px; border-radius: 12px; border: 1px solid #eee; text-align: center; }
.icon-big { font-size: 4rem; display: block; margin-bottom: 20px; }
h2 { color: #2c3e50; }
p { color: #666; }
</style>