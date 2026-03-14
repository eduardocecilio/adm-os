const API_URL = import.meta.env.VITE_API_URL || '/api';

/**
 * Wrapper genérico para chamadas API usando fetch.
 * @param {string} endpoint - O endpoint da API (ex: '/investimentos/swing-trade/calcular')
 * @param {object} options - Opções do fetch (method, body, headers, etc.)
 * @returns {Promise<any>} - A resposta JSON da API.
 */
async function api(endpoint, options = {}) {
    const url = `${API_URL}${endpoint}`;

    const token = localStorage.getItem('token');

    // Default headers
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    // Add Auth Header if token exists
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    // Auto-inject Workspace ID from URL if present
    // URL format: /<workspace_id>/route (e.g., /2/settings/general)
    const pathSegments = window.location.pathname.split('/').filter(Boolean);
    if (pathSegments.length > 0) {
        const potentialWorkspaceId = parseInt(pathSegments[0], 10);
        if (!isNaN(potentialWorkspaceId)) {
            headers['X-Workspace-Id'] = potentialWorkspaceId.toString();
        }
    }

    const config = {
        ...options,
        headers
    };

    if (config.body && typeof config.body === 'object') {
        config.body = JSON.stringify(config.body);
    }

    try {
        const response = await fetch(url, config);

        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('token');
                window.location.href = '/login';
                throw new Error("Sessão expirada. Faça login novamente.");
            }
            if (response.status === 404) throw new Error("Recurso não encontrado.");

            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Erro na requisição: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
}

export default api;
