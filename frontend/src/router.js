import { createRouter, createWebHistory } from 'vue-router'

import Home from './views/Home.vue'

// Importações de ESTRATÉGIA
import MenuEstrategia from './views/estrategia/MenuEstrategia.vue'
import NPS from './views/estrategia/NPS.vue'

// Importações de INVESTIMENTOS
import MenuInvestimentos from './views/investimentos/MenuInvestimentos.vue'
import SwingTrade from './views/investimentos/SwingTrade.vue'

// Importações de CONTABILIDADE
import MenuContabilidade from './views/contabilidade/MenuContabilidade.vue'
import Indicadores from './views/contabilidade/Indicadores.vue'
import BalancoPatrimonial from './views/contabilidade/BalancoPatrimonial.vue'
import DRE from './views/contabilidade/DRE.vue'

const routes = [
  { path: '/login', component: () => import('./views/auth/Login.vue') },
  { path: '/register', component: () => import('./views/auth/Register.vue') },
  { path: '/profile', component: () => import('./views/auth/Profile.vue'), meta: { requiresAuth: true } },

  {
    path: '/',
    component: Home,
    meta: { requiresAuth: true }
  },

  // Rotas de Investimentos
  { path: '/investimentos', component: MenuInvestimentos, meta: { requiresAuth: true } },
  { path: '/investimentos/swing-trade', component: SwingTrade, meta: { requiresAuth: true } },

  // Rotas de Contabilidade
  { path: '/contabilidade', component: MenuContabilidade, meta: { requiresAuth: true } },
  { path: '/contabilidade/indicadores', component: Indicadores, meta: { requiresAuth: true } },
  { path: '/contabilidade/balanco', component: BalancoPatrimonial, meta: { requiresAuth: true } },
  { path: '/contabilidade/dre', component: DRE, meta: { requiresAuth: true } },

  // Rotas de Estratégia
  { path: '/estrategia', component: MenuEstrategia, meta: { requiresAuth: true } },
  { path: '/estrategia/nps', component: NPS, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && token) {
    // If user is already logged in, redirect to home
    next('/')
  } else {
    next()
  }
})

export default router