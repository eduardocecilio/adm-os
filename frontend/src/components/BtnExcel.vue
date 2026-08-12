<script setup>
import { ref } from 'vue'
import api from '../services/api.js'

const props = defineProps({
  dados: { type: Object, required: true },
  tipo: { type: String, default: 'geral' } // 'geral', 'balanco', 'dre', 'indicadores'
})

const baixando = ref(false)

const downloadExcel = async () => {
  if (!props.dados) return
  baixando.value = true

  try {
    const blob = await api('/exportar/excel', {
      method: 'POST',
      body: { tipo: props.tipo, data: props.dados },
      responseType: 'blob'
    })

    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `relatorio_${props.tipo}_${new Date().toISOString().slice(0,10)}.xlsx`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)

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
