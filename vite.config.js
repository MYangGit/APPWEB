import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vitePluginString from 'vite-plugin-string'
import { viteAwesomeSvgLoader } from "vite-awesome-svg-loader";
import { createHtmlPlugin } from 'vite-plugin-html';


const getbuildOption = (mode) => {
  const build = {}
  let HtmlPlugin = []
  switch (mode) {
    case 'app':
      Reflect.set(build, 'outDir', 'packages/syslab/dist');
      HtmlPlugin = ["/md5.min.js", "/lodash.js"]
      break;
    case 'web':
      Reflect.set(build, 'outDir', 'packages/web/dist');
      break;
    case 'qt':
      Reflect.set(build, 'outDir', 'packages/web/dist');
      Reflect.set(build, 'target', 'chrome77');
      HtmlPlugin = ["/qwebchannel.js"]
      break;
    case 'desktop':
      Reflect.set(build, 'outDir', 'packages/desktop/dist');
      break;
    default:
      Reflect.set(build, 'outDir', 'dist');
      break;
  }
  return {
    build,
    HtmlPlugin
  }
}

// https://vitejs.dev/config/
export default defineConfig(({mode}) => {
  let customOption = getbuildOption(mode);
  return {
    plugins: [
      vue(),
      vitePluginString({
        include: [
          "**/*.md"
        ]
      }),
      viteAwesomeSvgLoader({
        defaultImport: "source-data-uri"
      }),
      createHtmlPlugin({
        inject: {
          data: {
            dynamicScripts: customOption.HtmlPlugin
          }
        }
      })
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
      extensions: ['.vue', '.js', '.ts']
    },
    build: {
      ...customOption.build,
    },
    server: {
      proxy: {
        '/gateway': {
          target: 'http://172.16.3.156:8080', // 后端地址
          changeOrigin: true, // 修改请求头中的 Origin 为目标域名
          rewrite: (path) => path.replace(/^\/api/, ''), // 移除路径中的 /api 前缀
        }
      }
    }
  }
})
