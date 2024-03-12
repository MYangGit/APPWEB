import { createRouter, createWebHistory } from 'vue-router'
import appDesigner from '../views/appDesigner.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: appDesigner
    }
  ]
})

export default router
