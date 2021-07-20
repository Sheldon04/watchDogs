import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/Login'
import Monitor from '../components/MonitorUser'
Vue.use(Router)

var router = new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/user/monitor',
      name: 'Monitor',
      component: Monitor
    }
  ]
})
export default router
