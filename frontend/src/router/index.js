import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Clientes from '../views/Clientes.vue'
import Portfolio from '../views/Portfolio.vue'
import Propostas from '../views/Propostas.vue'
import Eventos from '../views/Eventos.vue'
import Financeiro from '../views/Financeiro.vue'
import Ativos from '../views/Ativos.vue'
import Contratos from '../views/Contratos.vue'
import ContasReceber from '../views/ContasReceber.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Dashboard },
    { path: '/clientes', component: Clientes },
    { path: '/portfolio', component: Portfolio },
    { path: '/propostas', component: Propostas },
    { path: '/eventos', component: Eventos },
    { path: '/financeiro', component: Financeiro },
    { path: '/ativos', component: Ativos },
    { path: '/contratos', component: Contratos },
    { path: '/contas-receber', component: ContasReceber },
  ],
})

export default router