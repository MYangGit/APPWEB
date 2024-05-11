import { createRouter, createWebHashHistory } from 'vue-router'
import appDesigner from '../views/appDesigner.vue'
import Preview from '@/components/Editor/Preview.vue'


let routes = [
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

// 在main.js中引入router 使用动态 import() 不可用 在此处兼容 
let router 
if (import.meta.env.VITE_NODE_ENV === 'SyslabApp') {
  router = {}
}else {
  router = createRouter({
    history: createWebHashHistory(),
    routes
  })
}

export default router
