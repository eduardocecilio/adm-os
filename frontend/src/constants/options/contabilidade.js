// Opções para o Balanço Patrimonial
export const opcoesBalanco = {
  ac: [
    'Disponível (*)',             // mesmo que Caixa e Equivalentes, usado na Liquidez Imediata
    'Contas a Receber (*)',       // Usado no Prazo Médio de Recebimento (PMR)
    'Estoques (*)',               // Usado no Prazo Médio de Estocagem (PME)
    'Tributos a Recuperar', 
    'Outros Ativos', 
    'Despesas Antecipadas (*)'    // Usado na Liquidez Seca
  ],
  anc: [
    'Ativo Realizável a Longo Prazo (*)', // Usado na Liquidez Geral
    'Tributos a Recuperar (Longo Prazo)', 
    'Depósitos Judiciais', 
    'Outros Ativos (Longo Prazo)',
    'Investimentos', 
    'Imobilizado', 
    'Intangível',
    'Depreciação Acumulada'
  ],
  pc: [
    'Fornecedores (*)',                   // Usado no Prazo Médio de Pagamento (PMP)
    'Empréstimos e Financiamentos (*)',   // Usado no ROI (Investimento)
    'Obrigações Trabalhistas', 
    'Impostos, Taxas e Contribuições', 
    'Adiantamento de Clientes',
    'Lucros e Dividendos a Pagar',
    'Outras Obrigações'
  ],
  pnc: [
    'Empréstimos e Financiamentos (Longo Prazo) (*)', // Usado no ROI e Endividamento
    'Impostos, Taxas e Contribuições (Longo Prazo)',
    'Benefícios a Empregados',
    'Contingências',
    'Outros Passivos',
    'Provisões', 
    'Partes Relacionadas'
  ],
  pl: [
    'Capital Social', 
    'Reservas de Lucro', 
    'Reservas de Capital', 
    'Ajustes de Avaliação Patrimonial', 
    'Lucros/Prejuízos Acumulados'
  ]
}

// --- DRE ESTRUTURADA ---
export const opcoesDRE = {
  receita: [
    'Receita Bruta de Produtos (*)', // Usado no PMR
    'Venda de Mercadorias',
    'Prestação de Serviços'
  ],
  deducoes: [
    'Impostos sobre a Receita Bruta',
    'Devoluções',
    'Descontos Incondicionais'
  ],
  // Custos de Formação (CTO)
  custos_producao: [
    'Pessoal - CTO',
    'Serviços de Terceiros - CTO (*)', // Usado para calcular Compras
    'Depreciação e Amortização - CTO',
    'Insumos de Produção'
  ],
  // Custos de Venda (CMV)
  custos_venda: [
    'Custos dos Produtos e Mercadorias Vendidas',
    'CPV / CMV (*)' // Usado no PME e para calcular Compras
  ],
  // Despesas Comerciais (CML)
  desp_comerciais: [
    'Pessoal - CML',
    'Serviços de Terceiros - CML (*)', // Usado para calcular Compras
    'Depreciação e Amortização - CML',
    'Perdas Estimadas de Valores a Receber - CML',
    'Comissões',
    'Publicidade'
  ],
  // Despesas Administrativas (ADM)
  desp_administrativas: [
    'Pessoal - ADM',
    'Serviços de Terceiros - ADM (*)', // Usado para calcular Compras
    'Depreciação e Amortização - ADM',
    'Outras Despesas - ADM',
    'Aluguel',
    'Energia e Água'
  ],
  // Outras Ops
  outras_ops: [
    'Outras Receitas Operacionais',
    'Outras Despesas Operacionais'
  ],
  financeiro: [
    'Receitas Financeiras',
    'Despesas Financeiras',
    'Variação Cambial',
    'Juros sobre Capital Próprio'
  ],
  impostos: [
    'Imposto de Renda e Contribuição Social',
    'Provisão para IR/CS'
  ]
}