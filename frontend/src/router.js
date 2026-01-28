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

const routes = [
  { path: '/', component: Home },
  
  // Rotas de Investimentos
  { path: '/investimentos', component: MenuInvestimentos },
  { path: '/investimentos/swing-trade', component: SwingTrade },

  // Rotas de Contabilidade
  { path: '/contabilidade', component: MenuContabilidade },
  { path: '/contabilidade/indicadores', component: Indicadores },

  // Rotas de Estratégia
  { path: '/estrategia', component: MenuEstrategia },
  { path: '/estrategia/nps', component: NPS }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router