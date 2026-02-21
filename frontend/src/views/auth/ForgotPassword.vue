<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const handleForgotPassword = async () => {
    loading.value = true
    error.value = ''
    success.value = ''
    
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL || '/api'}/auth/forgot-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email.value })
        });
        
        const data = await response.json()
        
        if (!response.ok) {
            throw new Error(data.detail || 'Ocorreu um erro ao processar sua solicitação.')
        }

        success.value = data.msg || 'Se o e-mail existir, um link de recuperação será enviado.'
        email.value = '' // clear input
    } catch (err) {
        error.value = err.message
    } finally {
        loading.value = false
    }
}
</script>

<template>
  <div class="auth-wrapper">
    <!-- Esquerda: Imagem -->
    <div class="auth-image-side">
      <div class="overlay">
        <h2>Gestão Inteligente</h2>
        <p>Recupere seu acesso para continuar gerenciando seus negócios com a Adm OS.</p>
      </div>
    </div>

    <!-- Direita: Formulário -->
    <div class="auth-form-side">
      <div class="auth-card">
        <div class="logo-container">
          <h2>Adm OS</h2>
        </div>
        
        <div class="auth-header">
          <h3>Esqueci minha senha</h3>
          <p>Informe seu e-mail para receber um link de recuperação</p>
        </div>

        <form @submit.prevent="handleForgotPassword" class="auth-form">
          <div class="form-group">
            <label for="email">E-mail</label>
            <div class="input-wrapper">
              <i class="input-icon">✉️</i>
              <input 
                type="email" 
                id="email" 
                v-model="email" 
                required 
                placeholder="seu@email.com"
                autocomplete="email"
              >
            </div>
          </div>

          <div v-if="error" class="error-message">
            <i class="error-icon">⚠️</i> {{ error }}
          </div>
          <div v-if="success" class="success-message">
            <i class="success-icon">✅</i> {{ success }}
          </div>

          <button type="submit" class="btn-primary auth-btn" :disabled="loading" style="margin-top: 10px;">
            <span v-if="loading" class="spinner"></span>
            <span v-else>Enviar Link de Recuperação</span>
          </button>
        </form>

        <div class="auth-footer">
          <p>Lembrou da senha? <router-link to="/login">Voltar ao Login</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Reuse styles from Login.vue */
.auth-wrapper {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background-color: #f8fafc;
}

.auth-image-side {
  flex: 1;
  background-image: url('https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?q=80&w=2070&auto=format&fit=crop');
  background-size: cover;
  background-position: center;
  position: relative;
  display: none;
}

@media (min-width: 900px) {
  .auth-image-side {
    display: block;
  }
}

.overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(15, 23, 42, 0.4), rgba(15, 23, 42, 0.9));
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 4rem;
  color: white;
}

.overlay h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.overlay p {
  font-size: 1.125rem;
  opacity: 0.9;
  max-width: 400px;
  line-height: 1.6;
}

.auth-form-side {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  background: white;
  padding: 2.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.auth-logo {
  height: 48px;
  object-fit: contain;
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.auth-header p {
  color: #64748b;
  font-size: 0.875rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #334155;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: #94a3b8;
  font-size: 1.25rem;
  font-style: normal;
}

.input-wrapper input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  color: #0f172a;
  transition: all 0.2s;
  background-color: #f8fafc;
}

.input-wrapper input:focus {
  outline: none;
  border-color: #3b82f6;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.auth-btn {
  width: 100%;
  padding: 0.875rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 0.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s;
}

.auth-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.4);
}

.auth-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.auth-footer {
  margin-top: 2rem;
  text-align: center;
  font-size: 0.875rem;
  color: #64748b;
}

.auth-footer a {
  color: #3b82f6;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s;
}

.auth-footer a:hover {
  color: #2563eb;
  text-decoration: underline;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #fef2f2;
  color: #ef4444;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  border: 1px solid #fee2e2;
}

.success-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #f0fdf4;
  color: #16a34a;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  border: 1px solid #dcfce7;
}

.spinner {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
