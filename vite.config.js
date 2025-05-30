import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vitePluginString from 'vite-plugin-string'
import { viteAwesomeSvgLoader } from "vite-awesome-svg-loader";

const getbuildOption = (mode) => {
  const Option = {}
  switch (mode) {
    case 'app':
      Reflect.set(Option, 'outDir', 'packages/syslab/dist');
      break;
    case 'web':
      Reflect.set(Option, 'outDir', 'packages/web/dist');
      break;
    case 'qt':
      Reflect.set(Option, 'outDir', 'packages/web/dist');
      Reflect.set(Option, 'target', 'chrome77');
      break;
    case 'desktop':
      Reflect.set(Option, 'outDir', 'packages/desktop/dist');
      break;
    default:
      Reflect.set(Option, 'outDir', 'dist');
      break;
  }
  return Option
}

// https://vitejs.dev/config/
export default defineConfig(({mode}) => {
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
      })
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
      extensions: ['.vue', '.js', '.ts']
    },
    build: {
      ...getbuildOption(mode),
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
