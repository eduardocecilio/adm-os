<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useWorkspace } from '../composables/useWorkspace'
import api from '../services/api'

const router = useRouter()
const { activeWorkspace, setActiveWorkspace } = useWorkspace()

const workspaces = ref([])
const showDropdown = ref(false)

const loadWorkspaces = async () => {
  try {
    const data = await api('/workspaces/')
    workspaces.value = data
    
    // Fallback: If no active workspace is set but they exist, set the first one
    if (!activeWorkspace.value && data.length > 0) {
      setActiveWorkspace(data[0])
    }
  } catch (err) {
    console.error('Failed to load workspaces:', err)
  }
}

onMounted(() => {
  loadWorkspaces()
})

const selectWorkspace = (ws) => {
  setActiveWorkspace(ws)
  showDropdown.value = false
  // Força a navegação para a raiz do novo workspace
  router.push(`/${ws.id}/dashboard`)
}

const closeAndNavigate = (path) => {
  showDropdown.value = false
  router.push(path)
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('activeWorkspace')
  router.push('/login')
}
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <div class="logo" @click="router.push(`/${activeWorkspace.id}/dashboard`)">
        🚀 AdmOS
      </div>
      
      <!-- Workspace Switcher -->
      <div class="workspace-switcher" v-if="activeWorkspace">
        <div class="current-workspace" @click="showDropdown = !showDropdown">
          {{ activeWorkspace.name }}
          <span class="chevron">▼</span>
        </div>
        
        <div class="dropdown-menu clickup-style" v-if="showDropdown">
          <!-- Active Workspace Card -->
          <div class="active-ws-header">
            <div class="ws-info-top">
              <div class="ws-avatar">{{ activeWorkspace.name.charAt(0).toUpperCase() }}</div>
              <div class="ws-text">
                <span class="ws-name">{{ activeWorkspace.name }}</span>
                <span class="ws-role">{{ activeWorkspace.role === 'OWNER' ? 'Business' : activeWorkspace.role }}</span>
              </div>
            </div>
            <div class="ws-action-buttons">
              <button class="action-btn" @click="closeAndNavigate(`/${activeWorkspace.id}/settings/general`)">
                ⚙️ Configurações
              </button>
              <button class="action-btn" @click="closeAndNavigate(`/${activeWorkspace.id}/settings/members`)">
                👥 Pessoas
              </button>
            </div>
          </div>

          <div class="dropdown-divider"></div>

          <!-- Switch Workspaces -->
          <div class="switch-workspaces" v-if="workspaces.length > 1">
            <div class="section-label">Trocar de Workspace</div>
            <template v-for="ws in workspaces" :key="ws.id">
              <div 
                v-if="ws.id !== activeWorkspace.id"
                class="dropdown-item switch-item"
                @click="selectWorkspace(ws)"
              >
                <div class="ws-avatar-small">{{ ws.name.charAt(0).toUpperCase() }}</div>
                <span class="switch-ws-name">{{ ws.name }}</span>
              </div>
            </template>
            <div class="dropdown-divider"></div>
          </div>

          <!-- Note: /workspaces/new needs to be added to router if it doesn't exist -->
          <div class="dropdown-item create-new" @click="closeAndNavigate('/workspaces/new')">
            + Criar Espaço de trabalho
          </div>
        </div>
      </div>
    </div>
    
    <div class="actions">
      <button @click="router.push('/profile')" class="btn-profile">👤 Perfil</button>
      <button @click="logout" class="btn-logout">Sair</button>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: white;
  border-bottom: 1px solid #e0e0e0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
  margin-bottom: 2rem;
  position: relative;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  cursor: pointer;
}

/* Workspace Switcher Styles */
.workspace-switcher {
  position: relative;
}

.current-workspace {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  color: #334155;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s;
}

.current-workspace:hover {
  background: #f1f5f9;
  border-color: #94a3b8;
}

.chevron {
  font-size: 0.7rem;
  color: #94a3b8;
}

/* ClickUp Style Dropdown */
.dropdown-menu.clickup-style {
  position: absolute;
  top: calc(100% + 5px);
  left: 0;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  width: 320px;
  z-index: 100;
  padding: 16px 0 0 0;
  overflow: hidden;
}

.active-ws-header {
  padding: 0 16px 12px 16px;
}

.ws-info-top {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.ws-avatar {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: #10b981;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  font-weight: 700;
}

.ws-text {
  display: flex;
  flex-direction: column;
}

.ws-text .ws-name {
  font-weight: 600;
  color: #1e293b;
  font-size: 1.1rem;
}

.ws-text .ws-role {
  font-size: 0.85rem;
  color: #64748b;
}

.ws-action-buttons {
  display: flex;
  gap: 8px;
}

.action-btn {
  flex: 1;
  padding: 8px;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #475569;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
  color: #1e293b;
}

.section-label {
  font-size: 0.75rem;
  color: #94a3b8;
  font-weight: 600;
  padding: 8px 16px;
  margin-top: 4px;
}

.dropdown-item {
  padding: 12px 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  color: #334155;
  transition: background 0.2s;
}

.dropdown-item:hover {
  background: #f8fafc;
}

.switch-item {
  gap: 12px;
  padding: 10px 16px;
}

.switch-item:hover {
  background: #f1f5f9;
}

.ws-avatar-small {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: #0ea5e9;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
}

.switch-ws-name {
  font-weight: 500;
  font-size: 0.95rem;
}

.dropdown-divider {
  border-top: 1px solid #e2e8f0;
  margin: 0;
}

.create-new {
  color: #475569;
  justify-content: center;
  font-weight: 500;
  padding: 14px;
}

.create-new:hover {
  background: #f8fafc;
  color: #1e293b;
}

.actions { display: flex; gap: 10px; }

.btn-profile {
  background-color: transparent;
  color: #2c3e50;
  border: 1px solid #cbd5e1;
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}
.btn-profile:hover { background-color: #f8fafc; }

.btn-logout {
  background-color: transparent;
  color: #ef4444;
  border: 1px solid #fecaca;
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}

.btn-logout:hover {
  background: #fef2f2;
}

/* Responsive Design para Mobile */
@media (max-width: 768px) {
  .app-header {
    padding: 0.8rem 1rem;
    flex-wrap: wrap;
    gap: 0.8rem;
    margin-bottom: 1rem;
  }
  
  .header-left {
    width: 100%;
    justify-content: space-between;
    gap: 0.5rem;
  }
  
  .logo {
    font-size: 1.2rem;
  }
  
  .current-workspace {
    padding: 0.4rem 0.6rem;
    font-size: 0.85rem;
    max-width: 160px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .current-workspace .chevron {
    margin-left: 4px;
  }

  .actions {
    width: 100%;
    justify-content: flex-end;
    border-top: 1px solid #f1f5f9;
    padding-top: 0.8rem;
  }
  
  .btn-profile, .btn-logout {
    padding: 0.5rem 0.8rem;
    font-size: 0.85rem;
  }
  
  .dropdown-menu.clickup-style {
    position: fixed;
    top: 60px;
    left: 1rem;
    width: calc(100vw - 2rem);
    max-width: none;
    z-index: 1000;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.1);
  }
}
</style>
