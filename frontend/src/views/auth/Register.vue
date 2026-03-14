<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const workspaceName = ref('')

const inviteToken = ref(null)
const isInvited = ref(false)

const error = ref('')
const loading = ref(false)

const router = useRouter()
const route = useRoute()

onMounted(() => {
    const token = route.query.invite
    if (token) {
        try {
            // Unpack JWT payload statically (base64) to get email without relying on a full verifier
            const payload = JSON.parse(atob(token.split('.')[1]))
            if (payload.sub) {
                email.value = payload.sub
                inviteToken.value = token
                isInvited.value = true
            }
        } catch (e) {
            console.error("Invalid invite token format:", e)
        }
    }
})

const handleRegister = async () => {
    if (password.value.length < 8) {
        error.value = "A senha deve ter pelo menos 8 caracteres."
        return
    }

    if (password.value !== confirmPassword.value) {
        error.value = "As senhas não coincidem."
        return
    }

    loading.value = true
    error.value = ''

    try {
        const payload = {
            email: email.value,
            password: password.value
        }
        
        if (workspaceName.value) payload.workspace_name = workspaceName.value
        if (inviteToken.value) payload.invite_token = inviteToken.value

        const response = await fetch(`${import.meta.env.VITE_API_URL || '/api'}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })

        if (!response.ok) {
            const data = await response.json()
            throw new Error(data.detail || 'Falha ao registrar.')
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
  <div class="register-page">
    <div class="register-card">
      <div class="logo">🚀 AdmOS</div>
      <h1>Crie sua conta</h1>
      <p class="subtitle">Junte-se à plataforma gratuitamente</p>
      
      <form @submit.prevent="handleRegister">
        
        <div v-if="isInvited" class="invite-alert alert success">
            🎉 Você foi convidado para participar de um Workspace! Crie sua senha de acesso abaixo.
        </div>
      
        <div v-if="!isInvited" class="form-group">
          <label>Nome da sua Empresa / Organização</label>
          <input v-model="workspaceName" type="text" placeholder="Deixe em branco para preencher depois" />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" required placeholder="seu@email.com" :disabled="isInvited" :class="{'locked-input': isInvited}" />
        </div>

        <div class="form-group">
          <label>Senha</label>
          <input v-model="password" type="password" required placeholder="••••••••" />
        </div>

        <div class="form-group">
          <label>Confirmar Senha</label>
          <input v-model="confirmPassword" type="password" required placeholder="••••••••" />
        </div>

        <div v-if="error" class="error-msg">⚠️ {{ error }}</div>

        <button type="submit" :disabled="loading" class="btn-primary">
          {{ loading ? 'Criando conta...' : 'Registrar' }}
        </button>
      </form>
      
      <p class="footer-link">
        Já tem conta? <router-link to="/login">Entrar</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Copied styles from Login.vue for consistency */
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f6f8;
}

.register-card {
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
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #42b983;
  background: white;
  box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.1);
}

.btn-primary {
  width: 100%;
  padding: 14px;
  background-color: #2c3e50; /* A bit different for register to distinguish? Or keep Green? Let's use Dark Blue for variety or Green for consistency. Let's stick to Green or maybe Blue. User asked for visual identity. The logo is Blue text. Primary is Green. Let's use Green for consistency. */
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
