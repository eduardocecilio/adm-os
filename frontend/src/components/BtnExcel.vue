<script setup>
import { ref } from 'vue'

const props = defineProps({
  dados: { type: Object, required: true }, // O objeto do Balanço ou DRE
  tipo: { type: String, required: true },  // "balanco" ou "dre"
  nomeArquivo: { type: String, default: 'relatorio.xlsx' }
})

const loading = ref(false)

const baixarExcel = async () => {
  loading.value = true
  try {
    // 1. URL Dinâmica com Fallback
    const baseURL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001';

    const response = await fetch(`${baseURL}/exportar/excel`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 2. Token vindo das variáveis de ambiente (.env)
        'x-token': import.meta.env.VITE_API_TOKEN
      },
      body: JSON.stringify({
        dados: props.dados,
        tipo: props.tipo
      })
    })

    if (!response.ok) {
      if (response.status === 401) throw new Error("Não autorizado.");
      throw new Error("Erro ao gerar arquivo no servidor.");
    }

    // 1. Converte a resposta em BLOB (Arquivo Binário)
    const blob = await response.blob()
    
    // 2. Cria um link invisível no navegador
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = props.nomeArquivo 
    document.body.appendChild(a)
    
    // 3. Clica no link e remove
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)

  } catch (error) {
    alert("Erro ao baixar Excel: " + error.message)
    console.error(error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <button class="btn-excel" @click="baixarExcel" :disabled="loading">
    <span v-if="loading">⏳ Gerando...</span>
    <span v-else>📊 Baixar Excel</span>
  </button>
</template>

<style scoped>
/* Estilos mantidos - estão ótimos! */
.btn-excel {
  background-color: #217346; 
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: 0.2s;
  font-size: 0.95rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn-excel:hover {
  background-color: #1e6b41;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.15);
}

.btn-excel:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
  transform: none;
}
</style>