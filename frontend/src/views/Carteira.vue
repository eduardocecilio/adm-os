<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <div class="page">
    <header>
      <button @click="router.push('/')" class="back-btn">← Voltar</button>
      <h1>Gestão de Carteira</h1>
    </header>
    
    <div class="content">
      <p>Aqui entrarão os gráficos de Markowitz e Risco.</p>
    </div>
  </div>
</template>

<style scoped>
.page { padding: 40px; max-width: 800px; margin: 0 auto; }
header { display: flex; align-items: center; gap: 20px; margin-bottom: 40px; }
.back-btn { background: none; border: 1px solid #ccc; padding: 8px 16px; border-radius: 6px; cursor: pointer; }
.back-btn:hover { background: #eee; }
.content { background: white; padding: 40px; border-radius: 12px; border: 1px solid #eee; }
</style>