<template>
  <div id="plotapp">
    <div class="content_box">
      <div v-if="status === 'dynamic' && isReady === false" class="webagg-loading">
        <img :src="loadingGif" alt="">
        加载交互模式中...
      </div>
      <div class="static-img" v-show="status === 'static'">
        <img type="dynamic" :src="staticImgSrc" alt="" />
      </div>
      <div v-show="status === 'dynamic'" id="figure"> </div>
    </div>
    <div id="menu"></div>
  </div>
</template>

<script>
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet } from '@/utils/utils';

import loadingGif from '../../../packages/submodule/syslab_online_plot/lib/webagg/_images/loading.gif';
import '../../../packages/submodule/syslab_online_plot/lib/element/lib/theme-chalk/index.css'
import '../../../packages/submodule/syslab_online_plot/lib/lodash.js'
import '../../../packages/submodule/syslab_online_plot/lib/webagg/mpl.js'
import '../../../packages/submodule/syslab_online_plot/lib/webagg/color_change.js'
import '../../../packages/submodule/syslab_online_plot/lib/webagg/text_editor.js'
import '../../../packages/submodule/syslab_online_plot/lib/webagg/confirm_box.js'
import '../../../packages/submodule/syslab_online_plot/lib/webagg/_static/css/page.css'
import '../../../packages/submodule/syslab_online_plot/lib/webagg/_static/css/boilerplate.css'
import '../../../packages/submodule/syslab_online_plot/lib/webagg/_static/css/fbm.css'
import '../../../packages/submodule/syslab_online_plot/lib/webagg/_static/css/mpl.css'
import '../../../packages/submodule/syslab_online_plot/lib/webagg/_static/css/color_change.css'

let real = null
if (window.acquireVsCodeApi) {
  real = window.acquireVsCodeApi();
} else {
  real = window.parent;
}
const vscode =  {
  postMessage: function (message) {
    console.log('send:', message);
    real.postMessage(message);
  },
};

export default {
  props: {
    propValue: {
      type: Object,
      default: () => ({
        srcUrl: '',
      }),
    },
    element: {
      type: Object,
      default: () => {},
    },
  },
  data () {
    return {
      status: 'empty', //empty|static|dynamic
      staticImgSrc: '',
      figureId: '',
      imageBaseUrl: '',
      fig: undefined,
      port: '',
      ISONLINE: true,
      isReady: false,
      mouseMoveInterval:0,
      mouseDragInterval:0
    }
  },
  computed: {
    host() {
      return `${window.location.host}/syslabPlot`;
    },
    srcUrl: {
      get() {
        return getComputedGet('srcUrl', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
      },
      set(val) {
        getComputedSet('srcUrl', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
      }
    },
  },
  methods: {
    initFigure() {
      /* It is up to the application to provide a websocket that the figure
        will use to communicate to the server.  This websocket object can
        also be a "fake" websocket that underneath multiplexes messages
        from multiple figures, if necessary. 
      */
      if (this.fig) {
        return;
      }
      vscode.postMessage({ type: 'init_websocket' });
      let figId = this.figureId;
      window.oncontextmenu = (e) => {
        e.preventDefault();
        return false;
      };
      var fig = new mpl.figure(
        figId,
        document.getElementById('figure'),
        this.imageBaseUrl,
        vscode.postMessage,
        this.mouseMoveInterval,
        this.mouseDragInterval
      );
      this.fig = fig;
    },
    reconnectWebagg(figId) {
      if (this.fig) {
        vscode.postMessage({ type: 'init_websocket' });
      } else {
        this.initFigure();
      }
    },
    ondownload(figure, format) {
      // window.open('download.' + format, '_blank');
      vscode.postMessage({ type: 'download', value: format });
    },
    initWebaggFigure(status = 'static') {
      this.status = status;
      if (status === 'static') {
        return;
      }
      if (this.fig) {
        if (status === 'dynamic') {
          this.fig.send_message('refresh', {});
        }
        return;
      }
      vscode.postMessage({ type: 'initWebaggFigure' });
    },
    handleMessage(event) {
      console.log('receive:', event.data);
      const message = event.data;
      switch (message.type) {
        case 'loaded':{
          this.figureId = message.value;
          this.imageBaseUrl = message.imageBaseUrl;
          this.ISONLINE = message.ISONLINE;
          this.port = message.port;
          break;
        }
        case 'static_img': {
          if (this.status !== 'dynamic') {
            this.status = 'static';
            let new_src = message.value.includes('data:image')?message.value:'data:image/png;base64,' + message.value;
            if (new_src !== this.staticImgSrc) {
              this.staticImgSrc = new_src;
            }
          }
          break;
        }
        case 'mode_change': {
          this.initWebaggFigure(message.value);
          break;
        }
        case 'initFigure': {
          this.isReady=true;
          this.mouseMoveInterval = message.value.mouseMoveInterval;
          this.mouseDragInterval = message.value.mouseDragInterval;
          console.log('webagg',message.value);
          this.initFigure();
          break;
        }
        case 'figure_reset': {
          this.updateFigure();
          break;
        }
        case 'save_img': {
          if (this.staticImgSrc) {
            vscode.postMessage({
              type: 'save_img_res',
              value: this.staticImgSrc,
              status: true,
            });
          } else {
            vscode.postMessage({
              type: 'save_img_res',
              value: this.staticImgSrc,
              status: false,
            });
          }
          break;
        }
      }
    },
    updateFigure() {
      if (this.fig && this.figureId) {
        vscode.postMessage({ type: 'updateFigure' });
      }
    },
  },
  created() {
    document.addEventListener('contextmenu', function (_e) {
      _e.preventDefault();
      return false;
    });
    window.addEventListener('message', this.handleMessage);
    vscode.postMessage({ type: 'loaded' });
    vscode.postMessage({ type: 'hah', command: "toPlotService", value: 'hah1111' });
  }
}
</script>

<style>
  @font-face {
    font-family: 'iconfont';
    /* Project id 3893161 */
    src: url('https://at.alicdn.com/t/c/font_3893161_zb9qpcavc8.woff2?t=1676275315074') format('woff2'),
    url('https://at.alicdn.com/t/c/font_3893161_zb9qpcavc8.woff?t=1676275315074') format('woff'),
    url('https://at.alicdn.com/t/c/font_3893161_zb9qpcavc8.ttf?t=1676275315074') format('truetype');
  }

  #app {
    width: 100%;
    height: 100%;
    user-select: none;
  }

  .content_box {
    width: 100%;
    height: 100%;
    background-color: #f0f0f0;
  }

  #figure {
    height: 100%;
    width: 100%;
    flex: 1;
    min-height: 0;
    overflow: hidden;
  }

  .iconfont {
    font-family: 'iconfont' !important;
    font-size: 12px;
    font-style: normal;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  .icon-xiangyoujiantou:before {
    content: '\e65f';
  }

  .icon-checkbox-full:before {
    content: '\ea6f';
    font-size: 14px;
  }

  .icon-shixinyuan:before {
    content: '\e669';
  }

  .icon-sanjiaoxing:before {
    content: '\e615';
  }

  #menu {
    position: absolute;
    top: -500px;
    width: 122px;
    border: 1px solid #f3f3f3;
    padding: 5px 0;
    box-sizing: border-box;
    box-shadow: 2px 2px 8px rgb(0 0 0 / 20%);
    background-color: #f5f5f5;
    font-size: 12px;
    color: #333;
    z-index: 100;
    cursor: default;
  }

  .menu__item {
    padding: 5px 6px 5px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    /* height: 22px; */
    line-height: 1;
    position: relative;
  }
  .menu__item.disabled{
    color: #aaa;
    cursor: no-drop;
  }
  .submenu {
    padding: 5px 0;
    display: none;
    width: 100px;
    background-color: #fff;
    box-shadow: 2px 2px 8px rgb(0 0 0 / 20%);
    line-height: 1;
    position: absolute;
    height: fit-content;
    /* padding: 10px; */
    /* border: 1px solid #ddd; */
  }

  .submenu .submenu__item {
    /* border-bottom: 1px solid #ddd; */
    /* margin: 5px; */
    padding: 5px 6px 5px 24px;
    display: flex;
    align-items: center;
    color: #333;
    line-height: 1;
    position: relative;
    /* justify-content: space-between; */
  }
  .submenu__item .el-icon-check{
   position: absolute;
   left: 5px;
  }
  .menu__item:hover,
  .submenu__item:hover {
    background-color: #46a0fc;
    color: #fff;
  }
  .menu__item.disabled:hover{
    background-color: #d7d7d7;
    color: #aaa;
  }
  .submenu .iconfont {
    margin-right: 5px;
  }

  .menu__item:hover .submenu {
    display: block;
    position: absolute;
    right: -100px;
    /* top: 83px; */
  }

  .menu__item:hover .submenu2 {
    display: block;
    position: absolute;
    right: -100px;
    /* top: 103px; */
  }

  .menu__item:hover .submenu3 {
    display: block;
    position: absolute;
    right: -100px;
    /* top: 126px; */
  }

  .menu__item:hover .submenu4 {
    display: block;
    position: absolute;
    right: -100px;
    /* top: 147px; */
  }

  .menu__item:hover .submenu5 {
    display: block;
    position: absolute;
    right: -100px;
    /* top: 169px; */
  }

  .divider {
    width: 100%;
    height: 0;
    margin: 5px 0;
    border-bottom: 1px solid #e8e8e8;
  }

  .static-img {
    width: 100%;
    height: 99%;
    text-align: center;
  }

  .static-img img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    pointer-events: none;
  }

  .status_box {
    background-color: #e9e9e9;
    text-align: right;
    padding-right: 15px;
    display: flex;
    align-items: center;
  }

  .status_btn {
    /* border: none; */
    /* display: block; */
    width: 30px;
    height: 30px;
    font-size: 16px;
    margin: 5px 5px 5px 0;
  }

  .status_title {
    color: #333;
    flex: 1;
    text-align: center;
    padding-left: 10%;
  }

  .status_toolbar {
    width: 80px;
  }

  .webagg-loading {
    width: 100%;
    height: 100%;
    position: absolute;
    z-index: 99999;
    background-color: #fff;
    text-align: center;
    line-height: 1;
    font-size: 18px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 14px;
  }
  .webagg-loading img{
    width: 70px;
    margin: 10px;
  }
</style>
