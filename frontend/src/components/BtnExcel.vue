<script setup>
import { ref } from 'vue'

const props = defineProps({
  dados: { type: Object, required: true }, // O objeto do Balanço ou DRE
  dados: { type: Object, required: true },
  tipo: { type: String, default: 'geral' } // 'geral', 'balanco', 'dre', 'indicadores'
})

const baixando = ref(false)

const downloadExcel = async () => {
  if (!props.dados) return
  baixando.value = true

  try {
    // Usando api.js com opção de retornar o blob diretamente
    // Note: api.js might need adjustment to handle non-JSON responses if it defaults to response.json()
    // Let's check api.js again.
    // api.js uses response.json() by default. We need to pass a flag or handle it.
    // Let's look at api.js again to be sure.
    // It returns response.json().
    // I should probably modify api.js to handle blobs or just use fetch here with the correct URL from api.js export?
    // standard api.js usually returns json.
    // Let's update api.js to support blob or just use the relative URL logic here.
    // Actually, let's keep it simple and use the relative URL logic here for now, OR update api.js.
    // Updating api.js is cleaner.
    
    // For now, I will assume I can update api.js or just use the same URL logic.
    // The previous grep showed api.js: const API_URL = ...
    // I can export API_URL from api.js or just replicate the simple logic:
    
    const baseURL = import.meta.env.VITE_API_URL || '/api';
    
    const response = await fetch(`${baseURL}/exportar/excel`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-token': import.meta.env.VITE_API_TOKEN
      },
      body: JSON.stringify({ tipo: props.tipo, data: props.dados })
    });

    if (!response.ok) throw new Error("Falha ao gerar Excel")
    
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `relatorio_${props.tipo}_${new Date().toISOString().slice(0,10)}.xlsx`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)

  } catch (error) {
    console.error("Erro no download:", error)
    alert("Erro ao baixar Excel. Verifique o console.")
  } finally {
    baixando.value = false
  }
}
</script>

<template>
  <button class="btn-excel" @click="downloadExcel" :disabled="baixando">
    <span v-if="baixando">⏳ Gerando...</span>
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