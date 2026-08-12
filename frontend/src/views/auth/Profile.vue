<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api'
import Header from '../../components/Header.vue'
import { clearUserSession } from '../../services/session.js'

const router = useRouter()

const user = ref({
  email: '',
  id: null
})

const password = ref('')
const confirmPassword = ref('')
const currentPassword = ref('')
const message = ref('')
const error = ref('')
const loading = ref(false)

const fetchProfile = async () => {
  try {
    const data = await api('/users/me')
    user.value = data
  } catch (err) {
    error.value = "Erro ao carregar perfil."
  }
}

const updateProfile = async () => {
  if (!currentPassword.value) {
    error.value = "Informe sua senha atual para confirmar a alteração."
    return
  }

  if (password.value && password.value.length < 8) {
    error.value = "A nova senha deve ter pelo menos 8 caracteres."
    return
  }

  if (password.value && password.value !== confirmPassword.value) {
    error.value = "As senhas não coincidem."
    return
  }

  loading.value = true
  message.value = ''
  error.value = ''

  try {
    const payload = {
      email: user.value.email,
      current_password: currentPassword.value
    }

    if (password.value) {
      payload.password = password.value
    }

    const result = await api('/users/me', {
      method: 'PUT',
      body: payload
    })

    message.value = result.reauth_required
      ? "Credenciais atualizadas. Entre novamente para continuar."
      : "Perfil atualizado com sucesso!"
    password.value = ''
    confirmPassword.value = ''
    currentPassword.value = ''

    if (result.reauth_required) {
      clearUserSession()
      setTimeout(() => router.replace('/login'), 1200)
    }
  } catch (err) {
    error.value = err.message || "Erro ao atualizar perfil."
  } finally {
    loading.value = false
  }
}


onMounted(fetchProfile)
</script>

<template>
  <div class="page-container">
    <Header />

    <div class="content">
      <div class="profile-card">
        <h1>👤 Meu Perfil</h1>

        <form @submit.prevent="updateProfile">
          <!-- Dados Básicos -->
          <div class="form-group">
            <label>Email</label>
            <input v-model="user.email" type="email" required />
          </div>

          <div class="divider"></div>

          <div class="form-group">
            <label>Senha atual</label>
            <input
              v-model="currentPassword"
              type="password"
              autocomplete="current-password"
              required
              placeholder="Confirme sua senha atual"
            />
          </div>

          <!-- Alterar Senha -->
          <h3>Alterar Senha (Opcional)</h3>

          <div class="form-group">
            <label>Nova Senha</label>
            <input v-model="password" type="password" minlength="8" autocomplete="new-password" placeholder="Nova senha" />
          </div>

          <div class="form-group">
            <label>Confirmar Nova Senha</label>
            <input v-model="confirmPassword" type="password" minlength="8" autocomplete="new-password" placeholder="Confirme a nova senha" />
          </div>

          <!-- Mensagens e Botão (unificados) -->
          <div v-if="message" class="success-msg">✅ {{ message }}</div>
          <div v-if="error" class="error-msg">⚠️ {{ error }}</div>

          <button type="submit" :disabled="loading" class="btn-primary">
            {{ loading ? 'Salvando...' : 'Salvar Alterações' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-container { min-height: 100vh; background: #f4f6f8; }
.content { max-width: 600px; margin: 0 auto; padding: 20px; }

.profile-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

h1 { margin-top: 0; color: #2c3e50; }
h3 { color: #2c3e50; margin-bottom: 1rem; font-size: 1.1rem; }

.form-group { margin-bottom: 1.5rem; text-align: left; }
label { display: block; margin-bottom: 0.5rem; font-weight: 500; color: #2c3e50; }
input {
  width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #cbd5e1;
  font-size: 1rem; box-sizing: border-box;
}

.divider { height: 1px; background: #eee; margin: 2rem 0; }

.btn-primary {
  width: 100%; padding: 12px; background: #42b983; color: white; border: none;
  border-radius: 6px; font-size: 1rem; cursor: pointer;
}
.btn-primary:hover { background: #3aa876; }

.btn-secondary {
  padding: 10px 20px; background: #3b82f6; color: white; border: none;
  border-radius: 6px; cursor: pointer;
}
.btn-secondary:hover { background: #2563eb; }

.success-msg { color: #059669; background: #d1fae5; padding: 10px; border-radius: 6px; margin-bottom: 1rem; }
.error-msg { color: #ef4444; background: #fef2f2; padding: 10px; border-radius: 6px; margin-bottom: 1rem; }
</style>
