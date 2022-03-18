import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import Repositories from '../views/Repositories.vue'
import Backlog from '../views/Backlog.vue'
import Roadmap from '../views/Roadmap.vue'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/dashboards',
    name: 'Dashboards',
    component: Dashboard
  },
  {
    path: '/repos',
    name: 'Repositories',
    component: Repositories
  },
  {
    path: '/backlog',
    name: 'Backlog',
    component: Backlog
  },
  {
    path: '/roadmap',
    name: 'Roadmap',
    component: Roadmap
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
