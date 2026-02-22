<script setup>
import { ref, onMounted } from 'vue'
import Header from '../../components/Header.vue'
import { useWorkspace } from '../../composables/useWorkspace'
import api from '../../services/api'

const { activeWorkspace, getWorkspaceRole } = useWorkspace()
const inviteEmail = ref('')
const inviteRole = ref('MEMBER')
const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

// Para listar os membros no futuro, fariamos um fetch aqui
// const members = ref([]) 

const handleInvite = async () => {
  if (!inviteEmail.value) return
  
  loading.value = true
  errorMsg.value = ''
  successMsg.value = ''
  
  try {
    const response = await api(`/workspaces/${activeWorkspace.value.id}/invite`, {
      method: 'POST',
      body: {
        email: inviteEmail.value,
        role: inviteRole.value
      }
    })
    
    successMsg.value = response.msg || `Convite enviado para ${inviteEmail.value}`
    inviteEmail.value = ''
    
    // Se tivessemos lista de membros carregada, atualizariamos aqui.
  } catch (err) {
    errorMsg.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="settings-page">
    <Header />
    
    <div class="content-container">
      <div v-if="!activeWorkspace" class="no-workspace">
        <p>Carregando organização...</p>
      </div>
      
      <div v-else class="workspace-settings">
        <header class="settings-header">
          <h1>Pessoas e Acessos — {{ activeWorkspace.name }}</h1>
          <p class="subtitle">Gerencie quem tem acesso a esta organização.</p>
        </header>

        <div class="invite-card">
          <h3>Convidar novo membro</h3>
          <p class="helper-text">Eles precisarão criar uma conta usando o e-mail convidado.</p>
          
          <!-- Only Admin or Owner can see the invite form -->
          <form v-if="['OWNER', 'ADMIN'].includes(getWorkspaceRole())" @submit.prevent="handleInvite" class="invite-form">
            <div class="input-group">
              <input v-model="inviteEmail" type="email" placeholder="E-mail do colaborador" required />
              
              <select v-model="inviteRole">
                <option value="MEMBER">Membro</option>
                <option value="ADMIN">Administrador</option>
                <option value="GUEST">Convidado (Leitura)</option>
              </select>
              
              <button type="submit" class="btn-primary" :disabled="loading">
                {{ loading ? 'Enviando...' : 'Convidar' }}
              </button>
            </div>
            
            <div v-if="errorMsg" class="alert static error">⚠️ {{ errorMsg }}</div>
            <div v-if="successMsg" class="alert static success">✅ {{ successMsg }}</div>
            
          </form>
          
          <div v-else class="locked-state">
            <p>🔒 Apenas Administradores ou o Dono deste Workspace podem convidar novos usuários.</p>
          </div>
        </div>
        
      </div>
    </div>
  </div>
</template>

<style scoped>
.settings-page {
  min-height: 100vh;
  background-color: #f8fafc;
}

.content-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px 40px;
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

.invite-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.invite-card h3 {
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
}

input, select {
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  font-size: 1rem;
  color: #334155;
}

input { flex: 2; }
select { flex: 1; }

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
