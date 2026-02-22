<script setup>
import Header from '../../components/Header.vue'
import { useWorkspace } from '../../composables/useWorkspace'
import { useRoute, useRouter } from 'vue-router'

const { activeWorkspace } = useWorkspace()
const route = useRoute()
const router = useRouter()
</script>

<template>
  <div class="settings-layout">
    <Header />
    <div class="layout-body">
      <aside class="sidebar">
         <div class="sidebar-title">Gerenciar</div>
         <ul class="sidebar-menu">
           <li 
             :class="{ active: route.path.includes('/settings/general') }"
             @click="router.push('/settings/general')"
           >
             ⚙️ Configurações
           </li>
           <li 
             :class="{ active: route.path.includes('/settings/members') }"
             @click="router.push('/settings/members')"
           >
             👥 Pessoas
           </li>
         </ul>
      </aside>
      <main class="content">
        <header class="settings-header" v-if="activeWorkspace">
          <h1>{{ route.path.includes('general') ? 'Geral' : 'Pessoas' }} — {{ activeWorkspace.name }}</h1>
          <p class="subtitle">{{ route.path.includes('general') ? 'Gerencie as configurações fundamentais do seu Workspace.' : 'Gerencie quem tem acesso a esta organização.' }}</p>
        </header>
        
        <router-view />
      </main>
    </div>
  </div>
</template>

<style scoped>
.settings-layout {
  min-height: 100vh;
  background-color: #f8fafc;
}

.layout-body {
  display: flex;
  max-width: 1100px;
  margin: 0 auto;
  gap: 2rem;
  padding: 0 20px 40px;
}

.sidebar {
  width: 260px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  padding: 1.5rem 1rem;
  height: fit-content;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.sidebar-title {
  font-size: 0.8rem;
  text-transform: uppercase;
  font-weight: 700;
  color: #94a3b8;
  margin-bottom: 1rem;
  padding-left: 0.5rem;
  letter-spacing: 0.05em;
}

.sidebar-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-menu li {
  padding: 10px 12px;
  margin-bottom: 4px;
  border-radius: 8px;
  cursor: pointer;
  color: #475569;
  font-weight: 500;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.95rem;
}

.sidebar-menu li:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.sidebar-menu li.active {
  background: #eff6ff;
  color: #2563eb;
}

.content {
  flex: 1;
}

.settings-header {
  margin-bottom: 2rem;
}

.settings-header h1 {
  font-size: 1.8rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #64748b;
  font-size: 1.1rem;
}

/* Responsive Design para Mobile */
@media (max-width: 768px) {
  .layout-body {
    flex-direction: column;
    padding: 0 16px 20px;
    gap: 1.5rem;
  }

  .sidebar {
    width: 100%;
    box-sizing: border-box;
    padding: 1rem;
    height: auto;
  }

  .sidebar-menu {
    display: flex;
    gap: 10px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 8px; /* Espaço para a barra de rolagem */
  }

  .sidebar-menu li {
    margin-bottom: 0;
    white-space: nowrap;
    flex-shrink: 0;
  }

  .settings-header {
    margin-bottom: 1.5rem;
  }

  .settings-header h1 {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 1rem;
  }
}
</style>
