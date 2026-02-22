<script setup>
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const route = useRoute()

onMounted(async () => {
    try {
        const workspaces = await api('/workspaces/')
        if (workspaces && workspaces.length > 0) {
            // Find if there's a stored workspace ID that the user still has access to
            const storedWs = localStorage.getItem('activeWorkspace')
            let targetId = workspaces[0].id

            if (storedWs) {
                try {
                    const parsed = JSON.parse(storedWs)
                    if (workspaces.find(w => w.id === parsed.id)) {
                        targetId = parsed.id
                    }
                } catch (e) {
                    console.error("Error parsing stored workspace", e)
                }
            }
            
            // Redirect to the dashboard of the selected workspace
            // If they were trying to access a specific nested route (like invite link), 
            // the router logic in beforeEach handles that, this is just for the root "/"
            router.replace(`/${targetId}/dashboard`)
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
