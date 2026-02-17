import api from './api';

export default {
    /**
     * Calcula o resultado de uma operação de Swing Trade.
     * @param {Object} dados - { preco_compra, preco_venda, quantidade, taxa_corretagem }
     * @returns {Promise<Object>} - Resultado do cálculo
     */
    async calcularSwingTrade(dados) {
        return api('/investimentos/swing-trade/calcular', {
            method: 'POST',
            body: dados
        });
    }
};
