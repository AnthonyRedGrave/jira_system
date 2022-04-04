import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboards from '../views/Dashboards.vue'
import Repositories from '../views/Repositories.vue'
import Backlog from '../views/Backlog.vue'
import Roadmap from '../views/Roadmap.vue'
import Login from '../views/Login.vue'
import store from '@/store/index.js'



const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
        requiresAuth: true
    }
  },
  {
    path: '/login/',
    name: 'login',
    component: Login
  },
  {
    path: '/dashboards',
    name: 'Dashboards',
    component: Dashboards,
    meta: {
        requiresAuth: true
    }
  },
  {
    path: '/repos',
    name: 'Repositories',
    component: Repositories,
    meta: {
        requiresAuth: true
    }
  },
  {
    path: '/backlog',
    name: 'Backlog',
    component: Backlog,
    meta: {
        requiresAuth: true
    }
  },
  {
    path: '/roadmap',
    name: 'Roadmap',
    component: Roadmap,
    meta: {
        requiresAuth: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    if (!store.state.accessToken) {
      next({ name: 'login' })
      return
    }
    else{
      next()
    }
  }
  next()
  
})

export default router
