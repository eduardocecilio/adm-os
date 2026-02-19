<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'
import Header from '../../components/Header.vue'

const user = ref({
  email: '',
  id: null
})

const password = ref('')
const confirmPassword = ref('')
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
  if (password.value && password.value !== confirmPassword.value) {
    error.value = "As senhas não coincidem."
    return
  }

  loading.value = true
  message.value = ''
  error.value = ''

  try {
    const payload = {
      email: user.value.email
    }
    
    if (password.value) {
      payload.password = password.value
    }

    await api('/users/me', {
      method: 'PUT',
      body: payload
    })

    message.value = "Perfil atualizado com sucesso!"
    password.value = ''
    confirmPassword.value = ''
  } catch (err) {
    error.value = err.message || "Erro ao atualizar perfil."
  } finally {
    loading.value = false
  }
}

const sendTestEmail = async () => {
    try {
        await api('/users/send-test-email', { method: 'POST' })
        message.value = "Email de teste enviado! Verifique sua caixa de entrada (ou logs do servidor)."
    } catch (err) {
        error.value = "Erro ao enviar email."
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
          <div class="form-group">
            <label>Email</label>
            <input v-model="user.email" type="email" required />
          </div>

          <div class="divider"></div>
          <h3>Alterar Senha (Opcional)</h3>

          <div class="form-group">
            <label>Nova Senha</label>
            <input v-model="password" type="password" placeholder="Nova senha" />
          </div>

          <div class="form-group">
            <label>Confirmar Nova Senha</label>
            <input v-model="confirmPassword" type="password" placeholder="Confirme a nova senha" />
          </div>

          <div v-if="message" class="success-msg">✅ {{ message }}</div>
          <div v-if="error" class="error-msg">⚠️ {{ error }}</div>

          <button type="submit" :disabled="loading" class="btn-primary">
            {{ loading ? 'Salvando...' : 'Salvar Alterações' }}
          </button>
        </form>

        <div class="divider"></div>
        
        <div class="email-section">
            <h3>📧 Email</h3>
            <p>Teste as configurações de email enviando uma mensagem para você mesmo.</p>
            <button @click="sendTestEmail" class="btn-secondary">Enviar Email de Teste</button>
        </div>

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
