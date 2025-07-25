import './assets/main.css'
import './styles/reset.css';
import './styles/global.less'
import './assets/iconfont/iconfont.css';
import './assets/animate.less'

import { createApp } from 'vue'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import pinia from './stores/index.js';
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { install as CustomComponent } from '@/custom-component/index.js';
import Errantia from 'errantia'
import '../node_modules/errantia/dist/style.css'
import App from './App.vue'
import AppSyslab from './AppSyslab.vue';
import router from './router/index.js'
import { sizeDirect } from './directives/index.js'
import { isSyslabApp, isWebApp, isDesktop, isQt } from '@/utils/isPreviewOrApp'


const EnterApp = (isSyslabApp() || isWebApp() || isQt() || isDesktop()) ? AppSyslab : App
const app = createApp(EnterApp);

if (!isSyslabApp()) {
  app.use(router);
}

app.use(pinia)
app.directive('size-ob', sizeDirect)
app.use(ElementPlus)
app.use(CustomComponent)
app.use(Errantia)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.mount('#app')
