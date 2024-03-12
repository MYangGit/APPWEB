import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const usePageStore = defineStore('page', () => {
  const canvasStyleData = ref({
    // 页面全局数据
    width: 1600,
    height: 980,
    scale: 100,
    color: '#000',
    opacity: 1,
    background: '#fff',
    fontSize: 14,
    projectId: null,
    modelId: null,
    simulationTaskId: null,
    metaData: {},
  })
  const setCanvasStyle = (style) => {
    canvasStyleData.value = style;
  }
  return {
    canvasStyleData,
    setCanvasStyle
  }
})
