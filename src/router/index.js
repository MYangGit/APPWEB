import { createRouter, createWebHistory } from 'vue-router'
import appDesigner from '../views/appDesigner.vue'
import Preview from '@/components/Editor/Preview.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: appDesigner
    },
    {
      path: '/preview',
      name: 'preview',
      component: Preview
    }
  ]
})

export default router
