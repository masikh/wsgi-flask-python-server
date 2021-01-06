import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import CollapsableTable from '@/components/CollapsableTable'
import router from './router'
import store from './store'

Vue.config.productionTip = false

Vue.use(Buefy)
Vue.use(CollapsableTable)
Vue.use(VueAxios, axios)

new Vue({
  router,
  store,
  beforeCreate () {
    this.$http.defaults.baseURL = '/api'
    this.$store.commit('initialiseStore')
    if (this.$store.state.isLoggedIn) {
      this.$http.defaults.headers.common['Authorization'] = this.$store.state.token
    } else if (this.$router.currentRoute.path !== '/login') {
      this.$router.push('/login')
    }
  },
  created () {
    this.$http.interceptors.response.use(
      response => response,
      (error) => {
        if (error.response.status === 401) {
          this.$store.commit('logout')
          this.$router.push('/login')
        }
        return Promise.reject(error.response)
      })
    this.$router.beforeEach((to, from, next) => {
      if (to.name !== 'login' && !this.$store.state.isLoggedIn) {
        next({ name: 'login' })
      } else {
        next()
      }
    })
  },
  render: h => h(App)
}).$mount('#app')
