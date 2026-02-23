export const getMenuContabilidade = (workspaceId) => [
  { nome: 'Visão Geral', link: `/${workspaceId}/contabilidade` },
  { nome: 'Balanço Patrimonial', link: `/${workspaceId}/contabilidade/balanco` },
  { nome: 'DRE', link: `/${workspaceId}/contabilidade/dre` },
  { nome: 'Indicadores', link: `/${workspaceId}/contabilidade/indicadores` },
]