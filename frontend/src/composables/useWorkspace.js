import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

// Estado Global
const storedWs = localStorage.getItem('activeWorkspace')
let initialWorkspace = null

if (storedWs) {
    try {
        initialWorkspace = JSON.parse(storedWs)
    } catch {
        localStorage.removeItem('activeWorkspace')
    }
}

const activeWorkspace = ref(initialWorkspace)

export function useWorkspace() {
    const route = useRoute()

    // O setActiveWorkspace continua igual para gravações manuais/explícitas
    const setActiveWorkspace = (workspace) => {
        if (!workspace) return
        activeWorkspace.value = workspace
        localStorage.setItem('activeWorkspace', JSON.stringify(workspace))
    }

    const clearActiveWorkspace = () => {
        activeWorkspace.value = null
        localStorage.removeItem('activeWorkspace')
    }

    // Tentar ler da URL sempre que estiver disponível e mudar
    watch(
        () => route?.params?.workspaceId,
        (newId) => {
            if (newId && activeWorkspace.value && String(activeWorkspace.value.id) !== String(newId)) {
                // Aqui seria o ideal buscar do backend o novo workspace caso a gente
                // não tenha ele injetado no cache global, mas para não quebrar o SSR ou
                // loops infinitos, confiamos que os componentes que listam "meus workspaces"
                // (como o Header) vão puxar a lista completa e usar setActiveWorkspace
                // quando clicam no "selectWorkspace"
            }
        },
        { immediate: true }
    )

    const getWorkspaceRole = () => {
        return activeWorkspace.value ? activeWorkspace.value.role : null
    }

    const getWorkspaceId = () => {
        // Agora damos preferência absoluta para a URL se estivermos numa rota configurada,
        // senão pegamos o cacheado em memoria.
        if (route && route.params && route.params.workspaceId) {
            return route.params.workspaceId
        }
        return activeWorkspace.value ? activeWorkspace.value.id : null
    }

    return {
        activeWorkspace,
        setActiveWorkspace,
        clearActiveWorkspace,
        getWorkspaceRole,
        getWorkspaceId
    }
}
