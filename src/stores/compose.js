
import generateID from '@/utils/generateID'
import eventBus from '@/utils/eventBus'
import decomposeComponent from '@/utils/decomposeComponent'
import { $ } from '@/utils/utils'
import { commonStyle, commonAttr } from '@/custom-component/component-list'
import { createGroupStyle } from '@/utils/style'

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useDataCenterStore } from './dataCenter' 

export const useComposeStore = defineStore('compose', () => {
    const dataCenterStore = useDataCenterStore()
    const areaData = ref({
        style: {
            top: 0,
            left: 0,
            width: 0,
            height: 0,
        },
        components: [],
    })

    const editor = ref(null)

    const isActiveContainer = ref(null)

    const getEditor = () => {
        editor.value = $('#editor')
    }
    const setAreaData = (data) => {
        areaData.value = data
    }

    const setActiveContainer = (id) => {
        isActiveContainer.value = id;
    }

    const compose = ({ componentData, areaData, editor }) => {
        const components = []
        areaData.value.components.forEach(component => {
            if (component.component != 'Group') {
                components.push(component)
            } else {
                // 如果要组合的组件中，已经存在组合数据，则需要提前拆分
                const parentStyle = { ...component.style }
                const subComponents = component.propValue
                const editorRect = editor.getBoundingClientRect()

                subComponents.forEach(component => {
                    decomposeComponent(component, editorRect, parentStyle)
                })

                components.push(...component.propValue)
            }
        })

        const groupComponent = {
            id: generateID(),
            component: 'Group',
            label: '组合',
            icon: 'zuhe',
            ...commonAttr,
            style: {
                ...commonStyle,
                ...areaData.style,
            },
            propValue: components,
        }

        createGroupStyle(groupComponent)

        dataCenterStore.addComponent({
            component: groupComponent
        })
        eventBus.$emit('hideArea')
        batchDeleteComponent(dataCenterStore, areaData.components)
        dataCenterStore.setCurComponent({
            component: componentData[componentData.length - 1],
            index: componentData.length - 1,
        })

        areaData.components = []
    }

     // 将已经放到 Group 组件数据删除，也就是在 componentData 中删除，因为它们已经从 componentData 挪到 Group 组件中了
    const batchDeleteComponent = ({ componentData }, deleteData) => {
        deleteData.forEach(component => {
            for (let i = 0, len = componentData.length; i < len; i++) {
                if (component.id == componentData[i].id) {
                    componentData.splice(i, 1)
                    break
                }
            }
        })
    }

    const decompose = ({ curComponent, editor }) => {
        const parentStyle = { ...curComponent.style }
        const components = curComponent.propValue
        const editorRect = editor.getBoundingClientRect()
        dataCenterStore.deleteComponent()
        components.forEach(component => {
            decomposeComponent(component, editorRect, parentStyle)
            dataCenterStore.addComponent({component})
        })
    }
    return {
        isActiveContainer,
        areaData,
        editor,
        getEditor,
        setAreaData,
        setActiveContainer,
        batchDeleteComponent,
        compose,
        decompose
    }
})
