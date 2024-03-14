import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { deepCopy } from '@/utils/utils'
import { useDataCenterStore } from './dataCenter' 

export const useSnapShotStore = defineStore('snapshot', () => {
  const snapshotData = ref([])
  const snapshotIndex = ref(-1)
  const dataCenter = useDataCenterStore()
  const undo = () => {
    if (snapshotIndex.value >= 0) {
      snapshotIndex.value--
      const componentData = deepCopy(snapshotData.value[snapshotIndex.value]) || []
      if (dataCenter.curComponent) {
        // 如果当前组件不在 componentData 中，则置空
        const needClean = !componentData.find(component => dataCenter.curComponent.id === component.id)
        if (needClean) {
          dataCenter.setCurComponent({
            component: null,
            index: null,
          })
        }
      }
      dataCenter.setComponentData(componentData)
    }
  }
  const redo = () => {
    if (snapshotIndex.value < snapshotData.value.length - 1) {
      snapshotIndex.value++
      dataCenter.setComponentData(deepCopy(snapshotData.value[snapshotIndex.value]))
    }
  }
  const recordSnapshot = () => {
    // 添加新的快照
    snapshotData.value[++snapshotIndex.value] = deepCopy(dataCenter.componentData)
    // 在 undo 过程中，添加新的快照时，要将它后面的快照清理掉
    if (snapshotIndex.value < snapshotData.value.length - 1) {
      snapshotData.value = snapshotData.value.slice(0, snapshotIndex.value + 1)
    }
  }
  return {
    snapshotData,
    snapshotIndex,
    undo,
    redo,
    recordSnapshot
  }
})
