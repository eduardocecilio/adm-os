<script setup>
import { ref, onMounted, watch } from 'vue'
import { useWorkspace } from '../../composables/useWorkspace'
import api from '../../services/api'

const { activeWorkspace, getWorkspaceRole } = useWorkspace()

// Invite State
const inviteEmail = ref('')
const inviteRole = ref('MEMBER')
const loadingInvite = ref(false)
const inviteError = ref('')
const inviteSuccess = ref('')

// Members List State
const members = ref([])
const loadingMembers = ref(false)
const membersError = ref('')

const fetchMembers = async () => {
    if (!activeWorkspace.value) return
    loadingMembers.value = true
    try {
        const data = await api(`/workspaces/${activeWorkspace.value.id}/members`)
        members.value = data
    } catch (err) {
        membersError.value = "Erro ao carregar os membros: " + err.message
    } finally {
        loadingMembers.value = false
    }
}

const handleInvite = async () => {
  if (!inviteEmail.value) return
  loadingInvite.value = true
  inviteError.value = ''
  inviteSuccess.value = ''

  try {
    const response = await api(`/workspaces/${activeWorkspace.value.id}/invite`, {
      method: 'POST',
      body: {
        email: inviteEmail.value,
        role: inviteRole.value
      }
    })
    inviteSuccess.value = response.msg || `Convite enviado para ${inviteEmail.value}`
    inviteEmail.value = ''
    await fetchMembers()
  } catch (err) {
    inviteError.value = err.message
  } finally {
    loadingInvite.value = false
  }
}

const handleRemoveMember = async (userId) => {
    if (!confirm("Tem certeza que deseja remover este membro da organização?")) return
    try {
        await api(`/workspaces/${activeWorkspace.value.id}/members/${userId}`, {
            method: 'DELETE'
        })
        await fetchMembers()
    } catch (err) {
        alert(err.message)
    }
}

// Format date
const formatDate = (ds) => {
    return new Date(ds).toLocaleDateString('pt-BR')
}

// Watchers and Mounts
onMounted(() => {
    if (activeWorkspace.value) {
        fetchMembers()
    }
})

watch(activeWorkspace, (newVal) => {
    if (newVal) {
        fetchMembers()
    }
})

const isAdmin = () => ['OWNER', 'ADMIN'].includes(getWorkspaceRole())
</script>

<template>
  <div class="workspace-members">
      <div v-if="!activeWorkspace" class="no-workspace">
        <p>Carregando organização...</p>
      </div>

      <div v-else>
        <!-- Invite Panel -->
        <section class="settings-card">
          <h3>Convidar novo membro</h3>
          <p class="helper-text">Eles precisarão criar uma conta usando o e-mail convidado.</p>

          <form v-if="isAdmin()" @submit.prevent="handleInvite" class="invite-form">
            <div class="input-group">
              <input v-model="inviteEmail" type="email" placeholder="E-mail do colaborador" required />

              <select v-model="inviteRole">
                <option value="MEMBER">Membro</option>
                <option value="ADMIN">Administrador</option>
                <option value="GUEST">Convidado (Leitura)</option>
              </select>

              <button type="submit" class="btn-primary" :disabled="loadingInvite">
                {{ loadingInvite ? 'Enviando...' : 'Convidar' }}
              </button>
            </div>

            <div v-if="inviteError" class="alert static error">⚠️ {{ inviteError }}</div>
            <div v-if="inviteSuccess" class="alert static success">✅ {{ inviteSuccess }}</div>
          </form>

          <div v-else class="locked-state">
            <p>🔒 Apenas Administradores ou o Dono deste Workspace podem gerenciar membros.</p>
          </div>
        </section>

        <!-- Members Table -->
        <section class="settings-card">
          <h3>Membros Atuais</h3>
          <p class="helper-text">Pessoas que já possuem acesso a este Workspace.</p>

          <div v-if="loadingMembers">Carregando membros...</div>
          <div v-else-if="membersError" class="alert static error">{{ membersError }}</div>

          <div v-else class="table-container">
            <table class="members-table">
                <thead>
                    <tr>
                        <th>Usuário (Email)</th>
                        <th>Nível de Acesso</th>
                        <th>Data de Entrada</th>
                        <th v-if="isAdmin()">Ações</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="member in members" :key="member.user_id">
                        <td><strong>{{ member.email }}</strong></td>
                        <td><span class="badge" :class="member.role">{{ member.role }}</span></td>
                        <td>{{ formatDate(member.joined_at) }}</td>
                        <td v-if="isAdmin()">
                            <button
                                v-if="isAdmin() && member.role !== 'OWNER'"
                                @click="handleRemoveMember(member.user_id)"
                                class="btn-danger-text"
                            >
                                Remover
                            </button>
                            <span v-else class="text-muted">Proprietário</span>
                        </td>
                    </tr>
                </tbody>
            </table>
          </div>
        </section>
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

.btn-danger-text {
    background: transparent;
    border: none;
    color: #ef4444;
    font-weight: 600;
    cursor: pointer;
    font-size: 0.9rem;
}

.btn-danger-text:hover {
    text-decoration: underline;
}

.text-muted {
    color: #94a3b8;
    font-size: 0.9rem;
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

/* Table Styles */
.table-container {
    overflow-x: auto;
}

.members-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

.members-table th, .members-table td {
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid #e2e8f0;
}

.members-table th {
    background-color: #f8fafc;
    color: #475569;
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.members-table td {
    color: #334155;
    font-size: 0.95rem;
}

.badge {
    padding: 4px 8px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
}

.badge.OWNER { background: #fee2e2; color: #b91c1c; }
.badge.ADMIN { background: #e0e7ff; color: #4338ca; }
.badge.MEMBER { background: #d1fae5; color: #047857; }
.badge.GUEST { background: #f1f5f9; color: #475569; }

/* Responsive Design para Mobile */
@media (max-width: 768px) {
  .settings-card {
    padding: 1.2rem;
  }

  .input-group {
    flex-direction: column;
    gap: 0.8rem;
  }

  .btn-primary {
    width: 100%;
  }

  .settings-card h3 {
    font-size: 1.2rem;
  }

  .members-table th, .members-table td {
    padding: 10px 12px;
    font-size: 0.85rem;
  }

  .badge {
    font-size: 0.65rem;
  }
}
</style>
