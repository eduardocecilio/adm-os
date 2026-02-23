export const getMenuInvestimentos = (workspaceId) => [
  { nome: 'Visão Geral', link: `/${workspaceId}/investimentos` },
  { nome: 'Simulador Swing Trade', link: `/${workspaceId}/investimentos/swing-trade` },
  // { nome: 'Simulador Day Trade (Em breve)', link: '#' },
  // { nome: 'Estratégias de Opções (Em breve)', link: '#' }
]