import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // Importa nosso mapa

const app = createApp(App)
app.use(router) // Ativa o mapa
app.mount('#app')