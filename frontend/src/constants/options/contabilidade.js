// Opções para o Balanço Patrimonial
export const opcoesBalanco = {
  ac: [
    'Disponível',             // <--- Adicionado conforme sua planilha
    'Caixa e Equivalentes',   // <--- Mantido como sinônimo
    'Contas a Receber', 
    'Estoques', 
    'Tributos a Recuperar', 
    'Outros Ativos', 
    'Despesas Antecipadas'    // <--- Essencial para Liquidez Seca
  ],
  anc: [
    'Ativo Realizável a Longo Prazo', // <--- Essencial para Liquidez Geral
    'Tributos a Recuperar (Longo Prazo)', 
    'Depósitos Judiciais', 
    'Outros Ativos (Longo Prazo)',
    'Investimentos', 
    'Imobilizado', 
    'Intangível',
    'Depreciação Acumulada'
  ],
  pc: [
    'Fornecedores', 
    'Empréstimos e Financiamentos', 
    'Obrigações Trabalhistas', 
    'Impostos, Taxas e Contribuições', 
    'Adiantamento de Clientes',
    'Lucros e Dividendos a Pagar',
    'Outras Obrigações'
  ],
  pnc: [
    'Empréstimos e Financiamentos (Longo Prazo)', 
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

// Opções para a DRE
export const opcoesDRE = {
  receita: [
    'Receita Bruta de Vendas', 
    'Venda de Produtos', 
    'Venda de Serviços', 
    'Outras Receitas Operacionais'
  ],
  deducoes: [
    'Impostos sobre Vendas (ICMS/ISS/PIS/COFINS)', 
    'Devoluções de Vendas', 
    'Descontos Incondicionais', 
    'Abatimentos'
  ],
  custos: [
    'Custo dos Produtos Vendidos (CPV)', 
    'Custo das Mercadorias Vendidas (CMV)', 
    'Custo dos Serviços Prestados (CSP)', 
    'Custo de Estoque'
  ],
  despesas: [
    'Despesas com Pessoal', 
    'Salários e Encargos', 
    'Despesas Gerais e Administrativas', 
    'Aluguel e Condomínio', 
    'Marketing e Publicidade', 
    'Energia, Água e Internet', 
    'Depreciação e Amortização', 
    'Manutenção e Reparos', 
    'Software e Licenças'
  ],
  financeiro: [
    'Receitas Financeiras', 
    'Despesas Financeiras', 
    'Juros sobre Capital Próprio', 
    'Variação Cambial',
    'Descontos Obtidos',
    'Juros Pagos'
  ],
  impostos: [
    'IRPJ (Imposto de Renda)', 
    'CSLL (Contribuição Social)', 
    'Simples Nacional'
  ]
}