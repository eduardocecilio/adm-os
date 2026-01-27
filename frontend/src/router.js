import { createRouter, createWebHistory } from 'vue-router'

// Importando as páginas que criamos na pasta views
import Home from './views/Home.vue'
import Financeiro from './views/Financeiro.vue'
import Carteira from './views/Carteira.vue'
import Marketing from './views/Marketing.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/financeiro', component: Financeiro },
  { path: '/carteira', component: Carteira },
  { path: '/marketing', component: Marketing }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router