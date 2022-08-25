import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '../views/LayOut.vue'
import TestCase from '../views/TestCase.vue'
import TestTask from '../views/TestTask.vue'
import TestReport from '../views/TestReport.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/layout/testcase'
  },
  {
    path: '/layout',
    name: 'Layout',
    component: Layout,
    children: [
      {
        path: 'testcase',
        name: 'TestCase',
        component: TestCase
      },
      {
        path: 'task',
        name: 'TestTask',
        component: TestTask
      },
      {
        path: 'report',
        name: 'TestReport',
        component: TestReport
      },
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
