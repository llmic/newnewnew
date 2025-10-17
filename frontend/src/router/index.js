// src/router/index.js
import Vue from 'vue'  // 关键：添加这行导入Vue
import VueRouter from 'vue-router'
// 导入修改后的组件（确保路径正确）
import UserLogin from '../views/UserLogin.vue'
import UserRegister from '../views/UserRegister.vue'
import AppDashboard from '../views/AppDashboard.vue'
import { isAuthenticated } from '../services/auth'

// 必须在创建路由实例前调用 Vue.use()
Vue.use(VueRouter)  // 现在Vue已正确导入，可调用use方法

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: UserLogin,
    beforeEnter: (to, from, next) => {
      if (isAuthenticated()) {
        next('/dashboard')
      } else {
        next()
      }
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: UserRegister,
    beforeEnter: (to, from, next) => {
      if (isAuthenticated()) {
        next('/dashboard')
      } else {
        next()
      }
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: AppDashboard,
    beforeEnter: (to, from, next) => {
      if (isAuthenticated()) {
        next()
      } else {
        next('/login')
      }
    }
  }
]

// 创建路由实例
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router  // 导出路由实例