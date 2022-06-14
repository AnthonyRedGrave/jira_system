import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Dashboards from '../views/Dashboards.vue'
import Dashboard from '../views/Dashboard.vue'
import Repositories from '../views/Repositories.vue'
import Backlog from '../views/Backlog.vue'
import Roadmap from '../views/Roadmap.vue'
import Login from '../views/Login.vue'
import Notifications from '../views/Notifications.vue'
import Chats from '../views/Chats.vue'
import Chat from '../views/Chat.vue'
import Profile from '../views/Profile.vue'
import OtherProfile from '../views/OtherProfile.vue'  
import store from '@/store/index.js'


const ifAuth = (to, from, next) =>{
  if (!store.state.accessToken){
    next('/login')
    return
  }
  else{
    next()
  }
}


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    beforeEnter: ifAuth,
    meta: {
        
    }
  },
  {
    path: '/login/',
    name: 'login',
    component: Login
  },

  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    beforeEnter: ifAuth,
    meta: {
        requiresAuth: true
    }
  },
  {
    path: '/chats',
    name: 'Chats',
    component: Chats,
    beforeEnter: ifAuth,
    meta: {
        requiresAuth: true
    }
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat,
    beforeEnter: ifAuth,
    meta: {
        requiresAuth: true
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    beforeEnter: ifAuth,
    meta: {
        requiresAuth: true
    }
  },
  {
    path: '/profiles',
    name: 'OtherProfile',
    component: OtherProfile,
    beforeEnter: ifAuth,
    meta: {
        requiresAuth: true
    }
  },
  {
    path: '/dashboards',
    name: 'Dashboards',
    component: Dashboards,
    beforeEnter: ifAuth,
    meta: {
        requiresAuth: true
    }
  },
  {
    path: '/repos',
    name: 'Repositories',
    component: Repositories,
    beforeEnter: ifAuth,
    meta: {
        requiresAuth: true
    }
  },
  {
    path: '/backlog',
    name: 'Backlog',
    component: Backlog,
    beforeEnter: ifAuth,
    meta: {
        requiresAuth: true
    }
  },
  {
    path: '/roadmap',
    name: 'Roadmap',
    component: Roadmap,
    beforeEnter: ifAuth,
    meta: {
        requiresAuth: true
    }
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: Notifications,
    beforeEnter: ifAuth,
    meta: {
        requiresAuth: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// router.beforeEach((to, from, next) => {
//   if (to.meta.requiresAuth) {
//     if (!store.state.accessToken) {
//       next({ name: 'login' })
//       return
//     }
//     // else{
//     //   next()
//     // }
//   }
//   next()
  
// })

export default router
