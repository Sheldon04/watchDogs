import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/Login'
import Monitor from '../components/user/MonitorUser'
import TracebackUser from '../components/user/TracebackUser'
import AttackListUser from '../components/user/AttackListUser'
import AttackInfoUser from '../components/user/AttackInfoUser'
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
    },
    {
      path: '/user/traceback',
      name: 'TracebackUser',
      component: TracebackUser
    },
    {
      path: '/user/attacklist',
      name: 'AttackListUser',
      component: AttackListUser
    },
    {
      path: '/user/attackinfo',
      name: 'AttackInfoUser',
      component: AttackInfoUser
    }
  ]
})
export default router
