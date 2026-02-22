<script setup>
import { ref, onMounted, watch } from 'vue'
import { useWorkspace } from '../../composables/useWorkspace'
import api from '../../services/api'

const { activeWorkspace, getWorkspaceRole } = useWorkspace()

const newWorkspaceName = ref('')
const loadingRename = ref(false)
const renameError = ref('')
const renameSuccess = ref('')

const handleRenameWorkspace = async () => {
    if (!newWorkspaceName.value) return
    loadingRename.value = true
    renameError.value = ''
    renameSuccess.value = ''
    
    try {
        const data = await api(`/workspaces/${activeWorkspace.value.id}`, {
            method: 'PUT',
            body: { name: newWorkspaceName.value }
        })
        renameSuccess.value = "Nome da organização atualizado!"
        setTimeout(() => window.location.reload(), 1500)
    } catch (err) {
        renameError.value = err.message
    } finally {
        loadingRename.value = false
    }
}

onMounted(() => {
    if (activeWorkspace.value) {
        newWorkspaceName.value = activeWorkspace.value.name
    }
})

watch(activeWorkspace, (newVal) => {
    if (newVal) {
        newWorkspaceName.value = newVal.name
    }
})

const isAdmin = () => ['OWNER', 'ADMIN'].includes(getWorkspaceRole())
</script>

<template>
  <div class="workspace-general">
      <div v-if="!activeWorkspace" class="no-workspace">
        <p>Carregando organização...</p>
      </div>
      
      <div v-else>
        <section class="settings-card" v-if="isAdmin()">
          <h3>Geral</h3>
          <p class="helper-text">Altere as informações fundamentais da sua organização.</p>
          
          <form @submit.prevent="handleRenameWorkspace" class="inline-form">
              <div class="input-group">
                <input v-model="newWorkspaceName" type="text" placeholder="Nome do Workspace" required />
                <button type="submit" class="btn-primary" :disabled="loadingRename">
                    {{ loadingRename ? 'Salvando...' : 'Atualizar Nome' }}
                </button>
              </div>
              <div v-if="renameError" class="alert static error">⚠️ {{ renameError }}</div>
              <div v-if="renameSuccess" class="alert static success">✅ {{ renameSuccess }}</div>
          </form>
        </section>
        
        <div v-else class="locked-state">
            <p>🔒 Apenas Administradores ou o Dono deste Workspace podem gerenciar configurações gerais.</p>
        </div>
      </div>
  </div>
</template>

<style scoped>
.settings-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
}

.settings-card h3 {
  margin: 0 0 0.5rem 0;
  color: #0f172a;
}

.helper-text {
  color: #64748b;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.input-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  max-width: 600px;
}

input {
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  font-size: 1rem;
  color: #334155;
  flex: 3;
}

.btn-primary {
  padding: 12px 24px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background-color: #3aa876;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert.static {
  padding: 12px;
  border-radius: 8px;
  margin-top: 1rem;
  font-size: 0.95rem;
  max-width: 600px;
}

.alert.error {
  background-color: #fef2f2;
  color: #ef4444;
  border: 1px solid #fecaca;
}

.alert.success {
  background-color: #ecfdf5;
  color: #10b981;
  border: 1px solid #a7f3d0;
}

.locked-state {
  background: #f1f5f9;
  padding: 1rem;
  border-radius: 8px;
  color: #475569;
  text-align: center;
  font-weight: 500;
}
</style>
