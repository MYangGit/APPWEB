import './assets/main.css'
import './styles/reset.css';
import './styles/global.less'
import './assets/iconfont/iconfont.css';
import './assets/animate.less'

import { createApp } from 'vue'
import pinia from './stores/index.js';
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import '../node_modules/errantia/dist/style.css'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { install as CustomComponent } from '@/custom-component/index.js';

import Errantia from 'errantia'
import '../node_modules/errantia/dist/style.css'

import App from './App.vue'
import router from './router/index.js'


const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(ElementPlus)
app.use(CustomComponent)
app.use(Errantia)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.mount('#app')
