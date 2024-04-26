import toast from '@/utils/toast'
import generateID from '@/utils/generateID'
import { deepCopy } from '@/utils/utils'
import { ref } from 'vue'
import { rootStore } from './rootStore'
import { defineStore } from 'pinia'

export const useCopyStore = defineStore('copy', () => {
    const copyData = ref(null)
    const isCut = ref(false)
    // 恢复上一次剪切的数据
    const restorePreCutData = () => {
        if (isCut.value && copyData.value) {
            const data = deepCopy(copyData.value.data)
            const index = copyData.value.index
            rootStore.dataCenter.addComponent({ component: data, index })
            if (rootStore.dataCenter.curComponentIndex >= index) {
                // 如果当前组件索引大于等于插入索引，需要加一，因为当前组件往后移了一位
                rootStore.dataCenter.curComponentIndex++
            }
        }
    }

    const setCopyData = () => {
        copyData.value = {
            data: deepCopy(rootStore.dataCenter.curComponent),
            index: rootStore.dataCenter.curComponentIndex
        }
    }
    const copy = () => {
        if (!rootStore.dataCenter.curComponent) {
            toast('请选择组件')
            return
        }

        // 如果有剪切的数据，需要先还原
        restorePreCutData()
        setCopyData()

        isCut.value = false
    }
    const paste = (isMouse) => {
        if (!copyData.value) {
            toast('请选择组件')
            return
        }

        const data = copyData.value.data

        if (rootStore.compose.isActiveContainer) {
            const parent = rootStore.dataCenter.componentData.find(i => i.items?.some(j => j.name === state.isActiveContainer) || i.tabs?.some(j => j.name === state.isActiveContainer) || i.id === state.isActiveContainer);
            if (parent) {
                data.activeName = rootStore.compose.isActiveContainer;
                data.pid = parent.id;
            }
        }

        if (isMouse || rootStore.compose.isActiveContainer) {
            data.style.top = rootStore.contextmenu.menuTop
            data.style.left = rootStore.contextmenu.menuLeft
        } else {
            data.style.top += 10
            data.style.left += 10
        }

        if (data.component === 'Tabs') {
            data.tabs = data.tabs.map((i, j) => ({
                name: generateID(),
                label: i.label,
            }));
        } else if (data.component === 'GridLayout') {
            data.items = data.items.map((i, j) => ({
                name: generateID(),
                label: i.label,
            }));
        }
        if (component.component === 'ErGrid') {
            component.items = new Array(2).fill(1).map((i, j) => ({
                name: generateID(),
                label: `ErGrid${j + 1}`,
            }));
        }
        if(component.component === 'ErLayout') {
            const itemFlag = [
              { name: 'header', label: '页眉' },
              { name: 'leftSidebar', label: '左边栏' },
              { name: 'main', label: '主界面' },
              { name: 'rightSidebar', label: '右边栏' },
              { name: 'footer', label: '页脚' },
            ]
            component.items = new Array(5).fill(1).map((i, j) => ({
              name: generateID(),
              label: `ErLayout${itemFlag[j].name}`,
            }));
        }

        if(component.component === 'ErCollapse') {
            const itemFlag = [
                { name: 'only', label: '剩余空间' },
                { name: '1', label: '第一个cord' },
            ]
            component.items = new Array(itemFlag.length).fill(1).map((i, j) => ({
                name: generateID(),
                label:  `ErCollapse${itemFlag[j].name}`,
            }));
        }

        data.id = generateID()
        if (rootStore.dataCenter.componentData.filter(i => i.component === data.component).length) {
            data.label = data.label.replace(/\d*/g, '');
            data.label += rootStore.dataCenter.componentData.filter(i => i.component === data.component).length;
        }
        rootStore.dataCenter.addComponent({ component: deepCopy(data) })
        if (isCut.value) {
            copyData.value = null
        }
    }
    const cut = () => {
        if (!rootStore.dataCenter.curComponent) {
            toast('请选择组件')
            return
        }

        // 如果重复剪切，需要恢复上一次剪切的数据
        restorePreCutData()
        copyData()

        rootStore.dataCenter.deleteComponent()
        isCut.value = true
    }
    return {
        copy,
        paste,
        cut,
        isCut,
        copyData,
    }
})
