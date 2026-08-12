<script setup>
import { computed } from 'vue'

const props = defineProps({
  titulo: String,
  dados: Object, // { history: [], valor: '', variacao: 0 }
  periodoAtual: { type: String, default: '1M' },
  show: Boolean,
  exibirPeriodos: { type: Boolean, default: false } // <--- CONTROLE DOS BOTÕES
})

const emit = defineEmits(['close', 'trocarPeriodo'])

// Cálculos Matemáticos (Max, Min, Média)
const stats = computed(() => {
  const vals = props.dados.history || []
  if (vals.length === 0) return { max: 0, min: 0, avg: 0 }
  const max = Math.max(...vals)
  const min = Math.min(...vals)
  return { max, min, avg: (max + min) / 2 }
})

const formatEixo = (val) => new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 2, notation: "compact" }).format(val)
const chartColor = computed(() => (props.dados.variacao || 0) >= 0 ? '#27ae60' : '#c0392b')

// Desenho do SVG
const width = 600
const height = 250
const padding = 40

const getPath = () => {
  const points = props.dados.history || []
  if (points.length < 2) return ""

  const range = stats.value.max - stats.value.min || 1
  if (range === 0) return `M ${padding} ${height/2} L ${width} ${height/2}` // Linha reta

  const stepX = (width - padding) / (points.length - 1)
  let d = `M ${padding} ${height - ((points[0] - stats.value.min) / range) * height}`

  points.forEach((val, i) => {
    if (i === 0) return
    const x = padding + (i * stepX)
    const y = height - ((val - stats.value.min) / range) * height
    d += ` L ${x} ${y}`
  })
  return d
}
</script>

<template>
  <div v-if="show" class="modal-overlay" @click.self="emit('close')">
    <div class="modal-content">

      <div class="top-bar">
        <button class="close-btn" @click="emit('close')">×</button>
      </div>

      <div class="modal-header">
        <div class="header-main">
          <h2>{{ titulo }}</h2>

          <div class="modal-controls" v-if="exibirPeriodos">
            <button :class="{ active: periodoAtual === '1D' }" @click="emit('trocarPeriodo', '1D')">1D</button>
            <button :class="{ active: periodoAtual === '1M' }" @click="emit('trocarPeriodo', '1M')">1M</button>
            <button :class="{ active: periodoAtual === '1A' }" @click="emit('trocarPeriodo', '1A')">1A</button>
          </div>
        </div>

        <div class="modal-stats">
          <strong :style="{ color: chartColor }">{{ dados.valor }}</strong>
          <span v-if="dados.variacao !== undefined" :class="(dados.variacao || 0) >= 0 ? 'pos' : 'neg'">
            {{ (dados.variacao || 0) >= 0 ? '+' : '' }}{{ (dados.variacao || 0).toFixed(2) }}%
          </span>
        </div>
      </div>

      <div class="chart-big-container">
        <svg width="100%" height="100%" :viewBox="`0 -20 ${width} ${height + 40}`" preserveAspectRatio="none">
          <line :x1="padding" y1="1" :x2="width" y2="1" stroke="#e0e0e0" stroke-dasharray="4" />
          <text x="0" y="5" class="axis-text">{{ formatEixo(stats.max) }}</text>

          <line :x1="padding" :y1="height/2" :x2="width" :y2="height/2" stroke="#e0e0e0" stroke-dasharray="4" />
          <text x="0" :y="(height/2)+5" class="axis-text">{{ formatEixo(stats.avg) }}</text>

          <line :x1="padding" :y1="height-1" :x2="width" :y2="height-1" stroke="#e0e0e0" stroke-dasharray="4" />
          <text x="0" :y="height" class="axis-text">{{ formatEixo(stats.min) }}</text>

          <path :d="getPath()" fill="none" :stroke="chartColor" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" />
          <path :d="getPath() + ` L ${width} ${height} L ${padding} ${height} Z`" :fill="chartColor" opacity="0.1" stroke="none" />
        </svg>
      </div>

      <div class="modal-footer">
        <p v-if="exibirPeriodos">Variação no período selecionado.</p>
        <p v-else>Histórico baseado nos fechamentos salvos.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center;
  z-index: 1000; backdrop-filter: blur(4px);
}
.modal-content {
  background: white; width: 95%; max-width: 800px; padding: 15px 30px 30px 30px;
  border-radius: 16px; display: flex; flex-direction: column;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3); animation: slideUp 0.3s ease-out;
}
@keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

/* Layout Top Bar para o X */
.top-bar { display: flex; justify-content: flex-end; margin-bottom: 10px; }
.close-btn {
  border: none; background: none; font-size: 2rem; line-height: 0.5;
  cursor: pointer; color: #cbd5e0; transition: 0.2s; padding: 0;
}
.close-btn:hover { color: #e74c3c; transform: scale(1.1); }

.modal-header { margin-bottom: 20px; }
.header-main { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; margin-bottom: 10px; }
.header-main h2 { margin: 0; color: #2c3e50; font-size: 1.6rem; }

.modal-controls { display: flex; background: #f0f2f5; border-radius: 8px; padding: 4px; }
.modal-controls button {
  border: none; background: none; padding: 6px 14px; border-radius: 6px;
  cursor: pointer; font-weight: 600; color: #7f8c8d; transition: 0.2s; font-size: 0.9rem;
}
.modal-controls button:hover { color: #2c3e50; }
.modal-controls button.active { background: white; color: #2c3e50; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }

.modal-stats { display: flex; align-items: center; gap: 15px; }
.modal-stats strong { font-size: 2rem; line-height: 1; }
.modal-stats span { font-weight: bold; font-size: 1.1rem; padding: 4px 10px; border-radius: 6px; }
.pos { background: #e8f5e9; color: #27ae60; }
.neg { background: #ffebee; color: #c0392b; }

.chart-big-container { height: 300px; width: 100%; background: #ffffff; border: 1px solid #f0f0f0; border-radius: 12px; padding: 10px 20px 10px 0; box-sizing: border-box; }
.axis-text { font-size: 11px; fill: #95a5a6; font-family: monospace; }
.modal-footer { margin-top: 20px; text-align: center; color: #95a5a6; font-size: 0.85rem; border-top: 1px dashed #eee; padding-top: 15px; }

@media (max-width: 600px) {
  .header-main { flex-direction: column; align-items: flex-start; }
}
</style>