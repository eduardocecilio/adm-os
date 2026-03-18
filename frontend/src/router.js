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

import WorkspaceRedirector from './views/WorkspaceRedirector.vue'

const routes = [
  { path: '/login', component: () => import('./views/auth/Login.vue') },
  { path: '/register', component: () => import('./views/auth/Register.vue') },
  { path: '/forgot-password', component: () => import('./views/auth/ForgotPassword.vue') },
  { path: '/reset-password', component: () => import('./views/auth/ResetPassword.vue') },
  { path: '/profile', component: () => import('./views/auth/Profile.vue'), meta: { requiresAuth: true } },

  // O Root agora atua apenas como um interceptador para achar o Workspace correto
  {
    path: '/',
    component: WorkspaceRedirector,
    meta: { requiresAuth: true }
  },

  // Nova arquitetura Baseada em URL
  {
    path: '/:workspaceId',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        component: Home,
      },
      // Rotas de Workspaces / Configurações
      {
        path: 'settings',
        component: () => import('./views/settings/SettingsLayout.vue'),
        children: [
          { path: 'general', component: () => import('./views/settings/WorkspaceGeneral.vue') },
          { path: 'members', component: () => import('./views/settings/WorkspaceMembers.vue') },
          { path: '', redirect: to => `/${to.params.workspaceId}/settings/general` }
        ]
      },
      // Rotas de Investimentos
      { path: 'investimentos', component: MenuInvestimentos },
      { path: 'investimentos/swing-trade', component: SwingTrade },

      // Rotas de Contabilidade
      { path: 'contabilidade', component: MenuContabilidade },
      { path: 'contabilidade/indicadores', component: Indicadores },
      { path: 'contabilidade/balanco', component: BalancoPatrimonial },
      { path: 'contabilidade/dre', component: DRE },

      // Rotas de Estratégia
      { path: 'estrategia', component: MenuEstrategia },
      { path: 'estrategia/nps', component: NPS }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

import api from './services/api'

// Cache simples para não sobrecarregar as rotas com requests pro backend
let cachedWorkspaces = null

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('token')

  // 1. Verificação de Autenticação Básica
  if (to.meta.requiresAuth && !token) {
    return next('/login')
  }

  // 2. Bloqueio de Login/Register para usuários já logados
  if ((to.path === '/login' || to.path === '/register') && token) {
    return next('/')
  }

  // 3. Verificação de Segurança de Workspace (Role-Based Routing Guard)
  if (to.meta.requiresAuth && to.params && to.params.workspaceId) {
    const requestedId = to.params.workspaceId

    // Tenta ler do LocalStorage (injetado pelo Header/WorkspaceRedirector)
    const storedWsList = localStorage.getItem('userWorkspaces')

    try {
      if (storedWsList) {
        cachedWorkspaces = JSON.parse(storedWsList)
      } else if (!cachedWorkspaces) {
        // Fallback se o usuário der F5 muito rápido antes do LocalStorage salvar
        cachedWorkspaces = await api('/workspaces/')
      }

      const hasAccess = cachedWorkspaces.some(w => String(w.id) === String(requestedId))

      if (!hasAccess) {
        console.warn(`[Segurança] Usuário não tem acesso ao Workspace ${requestedId}. Redirecionando para segurança.`)
        return next('/') // Manda de volta pro Redirector que vai achar o Workspace correto dele
      }
    } catch (err) {
      console.error("Erro ao validar Workspace Authorization Guard", err)
      cachedWorkspaces = null
      return next('/login')
    }
  }

  next()
})

export default router