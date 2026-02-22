import { ref } from 'vue'

// Tenta pegar o workspace salvo no startup
const storedWs = localStorage.getItem('activeWorkspace')
const activeWorkspace = ref(storedWs ? JSON.parse(storedWs) : null)

export function useWorkspace() {

    const setActiveWorkspace = (workspace) => {
        activeWorkspace.value = workspace
        localStorage.setItem('activeWorkspace', JSON.stringify(workspace))
    }

    const getWorkspaceRole = () => {
        return activeWorkspace.value ? activeWorkspace.value.role : null
    }

    const getWorkspaceId = () => {
        return activeWorkspace.value ? activeWorkspace.value.id : null
    }

    return {
        activeWorkspace,
        setActiveWorkspace,
        getWorkspaceRole,
        getWorkspaceId
    }
}
