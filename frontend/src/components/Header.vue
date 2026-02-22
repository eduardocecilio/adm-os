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
  // Optional: reload the page or trigger a global event if data needs to refresh
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
      <div class="logo" @click="router.push('/')">
        🚀 AdmOS
      </div>
      
      <!-- Workspace Switcher -->
      <div class="workspace-switcher" v-if="activeWorkspace">
        <div class="current-workspace" @click="showDropdown = !showDropdown">
          {{ activeWorkspace.name }}
          <span class="chevron">▼</span>
        </div>
        
        <div class="dropdown-menu" v-if="showDropdown">
          <div 
            v-for="ws in workspaces" 
            :key="ws.id" 
            class="dropdown-item"
            :class="{ active: ws.id === activeWorkspace.id }"
            @click="selectWorkspace(ws)"
          >
            {{ ws.name }}
            <span class="role-badge">{{ ws.role }}</span>
          </div>
          <div class="dropdown-divider"></div>
          <div class="dropdown-item create-new" @click="router.push('/workspaces/new')">
            + Criar novo Workspace
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

.dropdown-menu {
  position: absolute;
  top: calc(100% + 5px);
  left: 0;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  width: 250px;
  z-index: 100;
  overflow: hidden;
}

.dropdown-item {
  padding: 12px 16px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #334155;
  font-weight: 500;
  transition: background 0.2s;
}

.dropdown-item:hover {
  background: #f8fafc;
}

.dropdown-item.active {
  background: #eff6ff;
  color: #2563eb;
  border-left: 3px solid #3b82f6;
}

.role-badge {
  font-size: 0.7rem;
  background: #e2e8f0;
  padding: 2px 6px;
  border-radius: 4px;
  color: #64748b;
  font-weight: 600;
}

.dropdown-divider {
  border-top: 1px solid #e2e8f0;
  margin: 4px 0;
}

.create-new {
  color: #42b983;
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
  background-color: #fef2f2;
}
</style>
