import { fileURLToPath, URL } from 'node:url'
import { viteAwesomeSvgLoader } from "vite-awesome-svg-loader";
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  return {
    plugins: [
      vue(),
      viteAwesomeSvgLoader({
        defaultImport: "source-data-uri"
      })
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
      extensions: ['.js', '.ts', '.jsx', '.tsx', '.json', '.vue'],
      build: {
        outDir: mode === 'app' ? 'packages/syslab/dist' : 'dist',
      }
    }

  } 
})
