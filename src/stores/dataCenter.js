import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { swap } from '@/utils/utils'
import toast from '@/utils/toast'

export const useDataCenterStore = defineStore('DataCenter', () => {
  const componentData = ref([])
  const curComponent = ref(null)
  const curComponentIndex = ref(null)

  const setComponentData = (data) => {
    componentData.value = data
  }

  const setCurComponent = ({component}) => {
    curComponent.value = component;
    let index = null;
    if (component) index = componentData.value.findIndex((i) => i.id === component.id);
    curComponentIndex.value = index;
  }

  const setShapeStyle = ({ top, left, width, height, rotate }) => {
    if (top) curComponent.value.style.top = Math.round(top);
    if (left) curComponent.value.style.left = Math.round(left);
    if (width) curComponent.value.style.width = width;
    if (height) curComponent.value.style.height = Math.round(height);
    if (rotate) curComponent.value.style.rotate = Math.round(rotate);
  }

  const setShapeSingleStyle = ({ key, value }) => {
    curComponent.value.style[key] = value;
  }

  // 添加组件
  const addComponent = ({ component, index }) => {
    if (index !== undefined) {
      componentData.value.splice(index, 0, component);
    } else {
      componentData.value.push(component);
    }
  }
  // 删除组件
  const deleteComponent = (index) => {
    if (index === undefined) {
      index = curComponentIndex.value;
    }

    if (index == curComponentIndex.value) {
      curComponentIndex.value = null;
      curComponent.value = null;
    }

    if (/\d/.test(index)) {
      componentData.value.splice(index, 1);
    }
  }

  const upComponent = () => {
    if (curComponentIndex.value < componentData.value.length - 1) {
      swap(componentData.value, curComponentIndex.value, curComponentIndex.value + 1)
      curComponentIndex.value++
    } else {
      toast('已经到顶了')
    }
  }
  
  const downComponent = () => {
    if (curComponentIndex.value > 0) {
      swap(componentData.value, curComponentIndex.value, curComponentIndex.value - 1)
      curComponentIndex.value--
    } else {
      toast('已经到底了')
    }
  }
  
  const topComponent = () => {
    if (curComponentIndex.value < componentData.value.length - 1) {
      componentData.value.splice(curComponentIndex.value, 1)
      componentData.value.push(curComponent.value)
      curComponentIndex.value = componentData.value.length - 1
    } else {
      toast('已经到顶了')
    }
  }
  
  const bottomComponent = () => {
    if (curComponentIndex.value > 0) {
      componentData.value.splice(curComponentIndex.value, 1)
      componentData.value.unshift(curComponent.value)
      curComponentIndex.value = 0
    } else {
      toast('已经到底了')
    }
  }

  return {
    componentData,
    curComponent,
    curComponentIndex,
    setComponentData,
    setCurComponent,
    setShapeStyle,
    setShapeSingleStyle,
    deleteComponent,
    addComponent,
    upComponent,
    downComponent,
    topComponent,
    bottomComponent
  }
})
