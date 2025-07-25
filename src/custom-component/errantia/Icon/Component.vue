<template>
    <div :class="{ 'disabled-container': disabled }">
        <component 
            v-if="iconComponent" 
            :is="iconComponent" 
            :class="{ 'disabled-container': disabled }"
            @click.stop="handleAction"
        />
        <span v-else>无</span>
    </div>
</template>

<script>
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet } from '@/utils/utils';
import { useEventCentre } from '@/hooks/useEventCentre';
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const { onClickOther } = useEventCentre();
export default {
    props: {
        propValue: {
            type: Object,
            default: () => ({
                activateText: "",
                className: '<el-icon><Setting /></el-icon>',
                disabled: false
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    computed: {
        iconComponent(){
            const match = this.className.match(/<(\w+)\s*\/>/)
            if (match && match[1]) {
                const iconName = match[1]
                if (ElementPlusIconsVue[iconName]) {
                    return ElementPlusIconsVue[iconName]
                }
            }
            return null
        },
        activateText: {
            get() {
                return getComputedGet('activateText', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('activateText', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        className: {
            get() {
                return getComputedGet('className', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('className', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        disabled: {
            get() {
                return getComputedGet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
    },
    methods: {
        handleAction(e) {
            e.stopPropagation();
            const { activateText } = this;
            const match = this.className.match(/<(\w+)\s*\/>/)
            onClickOther({element: this.element, clickName: 'click', params: { name: match[1], activateText }})
        },
    }
}
</script>

<style lang="less" scoped>
/* 禁用状态下的容器样式 */
.disabled-container {
  opacity: 0.5; /* 降低透明度 */
  pointer-events: none; /* 禁止鼠标事件 */
  cursor: not-allowed;    
}

/* 正常状态下的图标样式 */
.component {
  cursor: pointer; /* 鼠标指针变为手型 */
}
</style>
