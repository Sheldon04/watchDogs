import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/Login'
import Monitor from '../components/user/MonitorUser'
import TracebackUser from '../components/user/TracebackUser'
import AttackListUser from '../components/user/AttackListUser'
import AttackInfoUser from '../components/user/AttackInfoUser'
import MonitorAdmin from '../components/admin/MonitorAdmin'
import TracebackUserAdmin from '../components/admin/TracebackAdmin'
import AttackListUserAdmin from '../components/admin/AttackListAdmin'
import AttackInfoUserAdmin from '../components/admin/AttackInfoAdmin'

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
    },
    {
      path: '/admin/monitor',
      name: 'MonitorAdmin',
      component: MonitorAdmin
    },
    {
      path: '/admin/traceback',
      name: 'TracebackUserAdmin',
      component: TracebackUserAdmin
    },
    {
      path: '/admin/attacklist',
      name: 'AttackListUserAdmin',
      component: AttackListUserAdmin
    },
    {
      path: '/admin/attackinfo',
      name: 'AttackInfoUserAdmin',
      component: AttackInfoUserAdmin
    }
  ]
})
export default router
