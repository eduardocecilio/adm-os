<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 1. Variáveis para guardar o que o usuário digita
const form = ref({
  preco_compra: 0,
  preco_venda: 0,
  quantidade: 100,
  taxa_corretagem: 2.00
})

const resultado = ref(null) // Começa vazio

// 2. A Função que conecta com o Python (O Pulo do Gato)
async function calcularNoBackend() {
  try {
    // Envia o pedido para o seu servidor Python
    const resposta = await fetch('http://127.0.0.1:8000/calcular-resultado?tipo=normal', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value) // Transforma os dados em JSON
    })

    // Recebe a resposta do Python
    const dados = await resposta.json()
    resultado.value = dados // Guarda a resposta para mostrar na tela
    
  } catch (erro) {
    alert("Erro ao conectar com o servidor. O backend está rodando?")
    console.error(erro)
  }
}
</script>

<template>
  <div class="page">
    <header>
      <button @click="router.push('/')" class="back-btn">← Voltar</button>
      <h1>Simulador de Swing Trade</h1>
    </header>
    
    <div class="container">
      <div class="card input-area">
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
        
        <button @click="calcularNoBackend" class="btn-calcular">Calcular Lucro</button>
      </div>

      <div class="card resultado-area" v-if="resultado">
        <h3>Resultado da Operação</h3>
        
        <div class="resumo-item lucro">
          <span>Lucro Líquido:</span>
          <strong>R$ {{ resultado.resumo.lucro_liquido }}</strong>
        </div>
        
        <div class="detalhes">
          <p>Impostos (IR): R$ {{ resultado.resumo.imposto_renda }}</p>
          <p>Custos Totais: R$ {{ resultado.resumo.custos_totais }}</p>
          <p>Lucro Bruto: R$ {{ resultado.resumo.lucro_bruto }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page { padding: 40px; max-width: 1000px; margin: 0 auto; }
.container { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
.card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
.campo { margin-bottom: 20px; }
label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
.btn-calcular { width: 100%; background: #2c3e50; color: white; padding: 15px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; transition: 0.2s; }
.btn-calcular:hover { background: #42b983; }

.resumo-item { display: flex; justify-content: space-between; font-size: 1.5rem; border-bottom: 2px solid #eee; padding-bottom: 15px; margin-bottom: 15px; }
.lucro strong { color: #27ae60; }
.detalhes p { color: #666; margin: 5px 0; font-size: 0.9rem; }
</style>