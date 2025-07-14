<template>
    <div ref="container" class="bg preview">
        <ComponentWrapper 
            v-for="(item, index) in componentList.filter((i) => !i.pid)" 
            :key="index" 
            :config="item"
            :isShow="item.propValue?.isShow"
            :layoutType="layoutType" 
        />
        <!--  代码调用弹窗 -->
        <ConfirmBox/>
    </div>
</template>

<script>
import ComponentWrapper from './ComponentWrapper';
import ConfirmBox from '@/components/ConfirmBox.vue';
import { rootStore } from '@/stores/rootStore';
import { watch } from 'vue';
import { getValueByDotKey } from '@/utils/utils'
import { useGlobalUtils } from '@/hooks/useGlobalUtils';
import { excuteJsAction } from '@/hooks/useEventCentre';
import { isSyslabApp } from '@/utils/isPreviewOrApp'

const { initFilePath } = useGlobalUtils();
export default {
    components: { ComponentWrapper, ConfirmBox },
    props: {
        isScreenshot: {
            type: Boolean,
            default: false,
        },
        layoutType: {
            type: String,
            default: 'normal',
        },
    },
    data() {
        return {};
    },
    computed: {
        componentList () {
            return rootStore.dataCenter.componentData
        },
        watchRegisters () {
            return rootStore.dataConfig.watchRegisters
        },
        actionSet () {
            return rootStore.dataConfig.actionSet
        }
    },
    watch: {
        watchRegisters: {
            handler(val) {
                if (!val) return
                this.initWatch()
            },
            deep: true,
            immediate: true
        },
        actionSet:{
            handler(val) {
                if (!val) return
                this.initialize()
            },
            deep: true,
            immediate: true
        }
    },
    created() {
        rootStore.editor.setEditMode('preview')
        this.initialize();
    },
    methods: {
        isSyslabApp,
        pageInitAction () {
            let initActionNames = []
            for (const key in rootStore.dataConfig.actionSet) {
                if (key.indexOf('init_') === 0) {
                    initActionNames.push(key)
                }
            }
            initActionNames.forEach(async name => {
                excuteJsAction(name)
            })
        },
        initWatch () {
            rootStore.dataConfig.watchRegisters.forEach(({state, action, immediate}) => {
                watch(() => {
                    return getValueByDotKey(rootStore.dataConfig.stateSet, state.join('.'))
                }, (value) => {
                    excuteJsAction(action, {
                        property: state,
                        value
                    })
                }, { immediate:immediate, deep: true });
           })
        },
        async initialize() {
            if(isSyslabApp()){
                await initFilePath();
            }
            this.pageInitAction()
        },
    },
};
</script>

<style lang="less" scoped>
.bg {
    width: 100%;
    height: 100%;
    position: fixed;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
