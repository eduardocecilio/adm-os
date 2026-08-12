<script setup>
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../services/api'
import { useWorkspace } from '../composables/useWorkspace'

const router = useRouter()
const route = useRoute()
const { setActiveWorkspace } = useWorkspace()

onMounted(async () => {
    try {
        const workspaces = await api('/workspaces/')
        if (workspaces && workspaces.length > 0) {
            // Save allowed workspaces to LocalStorage for the Router Guard to read synchronously
            localStorage.setItem('userWorkspaces', JSON.stringify(workspaces))

            // Find if there's a stored workspace ID that the user still has access to
            const storedWs = localStorage.getItem('activeWorkspace')
            let targetWorkspace = workspaces[0]

            if (storedWs) {
                try {
                    const parsed = JSON.parse(storedWs)
                    const found = workspaces.find(w => String(w.id) === String(parsed.id))
                    if (found) {
                        targetWorkspace = found
                    }
                } catch (e) {
                    console.error("Error parsing stored workspace", e)
                }
            }

            // Set the active workspace globally so components (Home.vue, Header.vue) can use it
            setActiveWorkspace(targetWorkspace)

            // Redirect to the dashboard of the selected workspace
            router.replace(`/${targetWorkspace.id}/dashboard`)
        } else {
            // No workspaces found. Technically shouldn't happen due to auto-creation
            router.replace('/workspaces/new')
        }
    } catch (err) {
        console.error("Failed to load workspaces for redirection", err)
        router.replace('/login')
    }
})
</script>

<template>
    <div class="redirecting">
        <h2>Carregando seu espaço de trabalho...</h2>
    </div>
</template>

<style scoped>
.redirecting {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    color: #64748b;
}
</style>
