<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// Definimos o que esse componente aceita receber
defineProps({
  titulo: String,
  emoji: String,
  voltarPara: String, // Para onde o botão voltar aponta (ex: '/')
  itensMenu: Array    // Lista de links do menu lateral
})

const router = useRouter()

// Estado para controlar a visibilidade do menu
const menuAberto = ref(true)

function alternarMenu() {
  menuAberto.value = !menuAberto.value
}
</script>

<template>
  <div class="module-layout">

    <button
      v-if="!menuAberto"
      @click="alternarMenu"
      class="btn-abrir-menu"
      title="Abrir Menu"
    >
      ☰
    </button>

    <aside class="sidebar" :class="{ fechado: !menuAberto }">

      <button @click="alternarMenu" class="btn-fechar-menu" title="Esconder Menu">
        «
      </button>

      <div class="sidebar-header">
        <span class="emoji">{{ emoji }}</span>
        <h2>{{ titulo }}</h2>
      </div>

      <nav>
        <button
          v-for="item in itensMenu"
          :key="item.nome"
          @click="router.push(item.link)"
          class="menu-item"
        >
          {{ item.nome }}
        </button>

        <div class="divider"></div>

        <button @click="router.push(voltarPara || '/')" class="menu-item voltar">
          ← Voltar ao Início
        </button>
      </nav>
    </aside>

    <main class="content-area">
      <slot></slot>
    </main>
  </div>
</template>

<style scoped>
.module-layout { display: flex; min-height: 100vh; background-color: #f4f6f8; position: relative; }

/* --- BARRA LATERAL --- */
.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #ddd;
  padding: 30px;
  display: flex;
  flex-direction: column;
  position: relative; /* Para posicionar o botão de fechar */

  /* Animação Suave */
  transition: all 0.3s ease-in-out;
  overflow: hidden; /* Importante para o conteúdo não "vazar" enquanto fecha */
  white-space: nowrap; /* Impede que o texto quebre linha enquanto fecha */
}

/* Estado Fechado */
.sidebar.fechado {
  width: 0;
  padding: 0;
  border-right: none;
  opacity: 0;
}

/* Header e Itens */
.sidebar-header { margin-bottom: 40px; margin-top: 10px; }
.emoji { font-size: 3rem; display: block; margin-bottom: 10px; }
h2 { margin: 0; font-size: 1.5rem; color: #2c3e50; }

.menu-item {
  display: block;
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  padding: 12px 15px;
  margin-bottom: 5px;
  cursor: pointer;
  border-radius: 6px;
  color: #555;
  font-size: 1rem;
  font-weight: 500;
}
.menu-item:hover { background-color: #f0f0f0; color: #2c3e50; }
.voltar { color: #888; margin-top: auto; }
.voltar:hover { color: #d9534f; background: #fff5f5; }
.divider { height: 1px; background: #eee; margin: 20px 0; }

/* --- BOTÕES DE CONTROLE --- */

/* Botão de Fechar (dentro do menu) */
.btn-fechar-menu {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: 1px solid #eee;
  border-radius: 4px;
  cursor: pointer;
  color: #999;
  font-size: 1.2rem;
  padding: 2px 8px;
}
.btn-fechar-menu:hover { background: #f5f5f5; color: #333; }

/* Botão de Abrir (flutuante no conteúdo) */
.btn-abrir-menu {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10; /* Fica acima do conteúdo */
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 1.2rem;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  color: #555;
  transition: 0.2s;
}
.btn-abrir-menu:hover { background: #2c3e50; color: white; border-color: #2c3e50; }

/* --- ÁREA DE CONTEÚDO --- */
.content-area {
  flex: 1;
  padding: 40px;
  overflow-y: auto;
  transition: padding 0.3s; /* Suaviza se precisarmos ajustar padding */
}

/* Responsividade */
@media (max-width: 768px) {
  .module-layout { flex-direction: column; }
  .sidebar { width: 100%; height: auto; border-right: none; border-bottom: 1px solid #ddd; }
  .sidebar.fechado { height: 0; padding: 0; width: 100%; }

  /* No celular, o botão de abrir fica no topo fixo */
  .btn-abrir-menu { position: static; margin: 10px; width: auto; display: inline-block; }
}
</style>