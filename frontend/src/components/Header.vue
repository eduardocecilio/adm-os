<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<template>
  <header class="app-header">
    <div class="logo" @click="router.push('/')">
      🚀 AdmOS
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
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  cursor: pointer;
}

.actions { display: flex; gap: 10px; }

.btn-profile {
  background-color: transparent;
  color: #2c3e50;
  border: 1px solid #cbd5e1;
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
}
.btn-profile:hover { background-color: #f8fafc; }

.btn-logout {
  background-color: transparent;
  color: #ef4444;
  border: 1px solid #ef4444;
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
}

.btn-logout:hover {
  background-color: #fee2e2;
  color: #dc2626;
}
</style>
