<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const formData = new URLSearchParams()
    formData.append('username', email.value)
    formData.append('password', password.value)

    const response = await fetch(`${import.meta.env.VITE_API_URL || '/api'}/auth/token`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
    })

    if (!response.ok) {
        throw new Error('Login falhou. Verifique suas credenciais.')
    }

    const data = await response.json()
    localStorage.setItem('token', data.access_token)
    router.push('/')
    
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <div class="logo">🚀 AdmOS</div>
      <h1>Bem-vindo de volta</h1>
      <p class="subtitle">Faça login para continuar</p>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" required placeholder="seu@email.com" />
        </div>

        <div class="form-group">
          <label>Senha</label>
          <input v-model="password" type="password" required placeholder="••••••••" />
        </div>

        <div v-if="error" class="error-msg">⚠️ {{ error }}</div>

        <button type="submit" :disabled="loading" class="btn-primary">
          {{ loading ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>
      
      <p class="footer-link">
        Não tem conta? <router-link to="/register">Crie uma agora</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f6f8; /* Matches Global BG */
}

.login-card {
  background: white;
  padding: 3rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 420px;
  text-align: center;
  border: 1px solid #e0e0e0;
}

.logo {
  font-size: 2rem;
  font-weight: 800;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

h1 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #64748b;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: #2c3e50;
}

input {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  color: #2c3e50;
  font-size: 1rem;
  transition: all 0.2s;
  box-sizing: border-box; /* Essential for padding to be inside width */
}

input:focus {
  outline: none;
  border-color: #42b983; /* Vue Green */
  background: white;
  box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.1);
}

.btn-primary {
  width: 100%;
  padding: 14px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 1rem;
}

.btn-primary:hover:not(:disabled) {
  background-color: #3aa876;
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-msg {
  color: #ef4444;
  background: #fef2f2;
  padding: 10px;
  border-radius: 8px;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  text-align: left;
}

.footer-link {
  margin-top: 2rem;
  font-size: 0.9rem;
  color: #64748b;
}

.footer-link a {
  color: #42b983;
  text-decoration: none;
  font-weight: 600;
}

.footer-link a:hover {
  text-decoration: underline;
}
</style>
