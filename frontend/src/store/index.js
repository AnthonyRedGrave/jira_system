import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    accessToken: JSON.parse(localStorage.getItem('token')),
    refreshToken: null,
    username: JSON.parse(localStorage.getItem('username')),
    projects: []
  },
  mutations: {
    updateAuthCredentials(state, { access, refresh, username }) {
        state.accessToken = access
        state.refreshToken = refresh
        state.username = username
    },
    updateProjects(state, { projects }) {
        state.projects = projects
    },
    updateTasks(state, { tasks }){
        state.tasks = tasks
    }
  },
  getters:{
    loggedIn(state) {
        return state.accessToken != null
    }
  },
  actions: {
    userLogin(context, usercredential) {
            return new Promise((resolve, reject) => {
                axios({
                        method: 'post',
                        url: 'http://localhost:8000/api/token/',
                        data: {
                            username: usercredential.username,
                            password: usercredential.password
                        },
                        credentials: 'include',
                    }).then((responce) => {
                        context.commit('updateAuthCredentials', { access: responce.data.access, refresh: responce.data.refresh, username: usercredential.username })
                        localStorage.setItem('token', JSON.stringify(responce.data.access))
                        localStorage.setItem('username', JSON.stringify(usercredential.username))

                        resolve(responce)
                    })
                    .catch(err => {
                        console.log(err)
                        reject(err)
                    })
            })

        },
    getProjects(context, access) {
            return new Promise((resolve, reject) => {
                axios({
                        method: 'get',
                        url: 'http://localhost:8000/api/projects/',
                        headers: { Authorization: `Bearer ${access.token}` },
                        credentials: 'include',
                    }).then((responce) => {
                        context.commit('updateProjects', { projects: responce.data })
                        resolve(responce)
                    })
                    .catch(err => {
                        console.log(err)
                        reject(err)
                    })
            })
        },
    getTasks(context, access) {
            return new Promise((resolve, reject) => {
                axios({
                        method: 'get',
                        url: 'http://localhost:8000/api/tasks/',
                        headers: { Authorization: `Bearer ${access.token}` },
                        credentials: 'include',
                    }).then((responce) => {
                        context.commit('updateTasks', { projects: responce.data })
                        resolve(responce)
                    })
                    .catch(err => {
                        console.log(err)
                        reject(err)
                    })
            })
        },
  },
  modules: {
  }
})
