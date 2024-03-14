import './assets/main.css'
import './styles/reset.css';
import './styles/global.less'
import './assets/iconfont/iconfont.css';
import './assets/animate.less'

import { createApp } from 'vue'
import pinia from './stores';

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { install as CustomComponent } from '@/custom-component';

import App from './App.vue'
import router from './router'


const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(ElementPlus)
app.use(CustomComponent)

app.mount('#app')
