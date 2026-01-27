<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref({
  preco_compra: 0,
  preco_venda: 0,
  quantidade: 100,
  taxa_corretagem: 2.00
})

const resultado = ref(null)

async function calcularNoBackend() {
  try {
    const resposta = await fetch('http://127.0.0.1:8000/calcular-resultado?tipo=normal', {
      method: 'POST',
      headers: { 
              'Content-Type': 'application/json',
              'x-token': 'admin-os-segredo-2026'
            },
      body: JSON.stringify(form.value)
    })
    const dados = await resposta.json()
    resultado.value = dados 
  } catch (erro) {
    alert("Erro ao conectar com o servidor. Verifique se o backend está rodando.")
    console.error(erro)
  }
}
</script>

<template>
  <div class="page">
    <header>
      <button @click="router.push('/')" class="back-btn">← Voltar</button>
      <h1>Carteira & Risco</h1>
    </header>
    
    <div class="container">
      <div class="card input-area">
        <h2>Simulador de Swing Trade</h2>
        <p class="desc">Calcule o lucro líquido descontando IR e Taxas da B3.</p>
        
        <div class="campo">
          <label>Preço de Compra (R$)</label>
          <input type="number" v-model="form.preco_compra" step="0.01">
        </div>
        <div class="campo">
          <label>Preço de Venda (R$)</label>
          <input type="number" v-model="form.preco_venda" step="0.01">
        </div>
        <div class="campo">
          <label>Quantidade</label>
          <input type="number" v-model="form.quantidade">
        </div>
        
        <button @click="calcularNoBackend" class="btn-calcular">Calcular Resultado</button>
      </div>

      <div class="card resultado-area" v-if="resultado">
        <h3>Resumo da Operação</h3>
        
        <div class="resumo-item lucro">
          <span>Lucro Líquido:</span>
          <strong>R$ {{ resultado.resumo.lucro_liquido }}</strong>
        </div>
        
        <div class="detalhes">
          <p>Imposto de Renda (15%): R$ {{ resultado.resumo.imposto_renda }}</p>
          <p>Custos (Corretagem + B3): R$ {{ resultado.resumo.custos_totais }}</p>
          <p>Lucro Bruto: R$ {{ resultado.resumo.lucro_bruto }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page { padding: 40px; max-width: 1000px; margin: 0 auto; }
header { display: flex; align-items: center; gap: 20px; margin-bottom: 40px; }
.back-btn { background: white; border: 1px solid #ccc; padding: 8px 16px; border-radius: 6px; cursor: pointer; color: #555; }
.back-btn:hover { background: #eee; }

.container { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
/* Responsividade: vira uma coluna só em celular */
@media (max-width: 768px) { .container { grid-template-columns: 1fr; } }

.card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); height: fit-content; }
.desc { color: #666; font-size: 0.9rem; margin-bottom: 20px; }
h2 { margin-top: 0; color: #2c3e50; }

.campo { margin-bottom: 20px; }
label { display: block; margin-bottom: 5px; font-weight: 600; color: #2c3e50; }
input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
input:focus { border-color: #42b983; outline: none; }

.btn-calcular { width: 100%; background: #2c3e50; color: white; padding: 15px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; transition: 0.2s; font-weight: bold; }
.btn-calcular:hover { background: #42b983; }

.resumo-item { display: flex; justify-content: space-between; font-size: 1.5rem; border-bottom: 2px solid #eee; padding-bottom: 15px; margin-bottom: 15px; margin-top: 20px; }
.lucro strong { color: #27ae60; }
.detalhes p { color: #666; margin: 8px 0; font-size: 0.95rem; display: flex; justify-content: space-between; }
</style>