<template>
    <div ref="container" class="bg preview">
        <ComponentWrapper 
            v-for="(item, index) in copyData.filter((i) => !i.pid)" 
            :key="index" 
            :config="item" 
        />
    </div>
</template>

<script>
import { getStyle, getCanvasStyle } from '@/utils/style';
import localforage from 'localforage';
import ComponentWrapper from './ComponentWrapper';
import { changeStyleWithScale } from '@/utils/translate';
import { toPng } from 'html-to-image';
import { rootStore } from '@/stores/rootStore';
import { watch } from 'vue';
import { getValueByDotKey } from '@/utils/utils'
import { useGlobalUtils } from '@/hooks/useGlobalUtils';
import { useEventCentre } from '@/hooks/useEventCentre';

const { initFilePath } = useGlobalUtils();
const { onInit } = useEventCentre();
export default {
    components: { ComponentWrapper },
    props: {
        isScreenshot: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            copyData: [],
            canvasStyleData: {},
        };
    },
    created() {
        this.initialize();
        if(import.meta.env.VITE_NODE_ENV === 'SyslabApp') {
            this.copyData = rootStore.dataCenter.componentData
            this.canvasStyleData = rootStore.page.canvasStyleData
        }else {
            localforage.getItem('canvasData').then((data) => {
            this.copyData = JSON.parse(data) || [];
            });
            localforage.getItem('canvasStyle').then((data) => {
                this.canvasStyleData = JSON.parse(data);
            });
        }
        rootStore.editor.setEditMode('preview')
        setTimeout(() => {
            this.initWatch()
        }, 1000)
    },
    methods: {
        getStyle,
        getCanvasStyle,
        changeStyleWithScale,
        pageInitAction () {
            let fnStrs = []
            for (const key in rootStore.dataConfig.actionSet) {
                if (key.indexOf('init_') === 0) {
                    fnStrs.push(rootStore.dataConfig.actionSet[key])
                }
            }
            fnStrs.forEach(async fnStr => {
                onInit({type: 'init', fnStr})
            })
        },
        close() {
            this.$emit('close');
        },
        htmlToImage() {
            toPng(this.$refs.container.querySelector('.canvas'))
                .then((dataUrl) => {
                    const a = document.createElement('a');
                    a.setAttribute('download', 'screenshot');
                    a.href = dataUrl;
                    a.click();
                })
                .catch((error) => {
                    console.error('oops, something went wrong!', error);
                })
                .finally(this.close);
        },
        initWatch () {
            //todo： 有空建议移动到hooks中事件中心
            rootStore.dataConfig.watchRegisters.forEach(({state, action}) => {
                let fn = new Function(`return ${rootStore.dataConfig.actionSet[action]}`)()
                watch(() => {
                    return getValueByDotKey(rootStore.dataConfig.stateSet, state.join('.'))
                }, (value) => {
                    fn({ 
                        dataCenter: rootStore.dataConfig.stateSet,
                        globalUtils: {}
                    }, {
                        value
                    })
                }, { deep: true });
           })
        },
        async initialize() {
            await initFilePath();
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

    .canvas-container {

        .canvas {
            background: #fff;
            position: relative;
            margin: auto;
        }
    }

    .close {
        position: absolute;
        right: 20px;
        top: 20px;
    }
}
</style>
