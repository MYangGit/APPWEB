<template>
    <div ref="container" class="bg preview">
        <ComponentWrapper 
            v-for="(item, index) in copyData.filter((i) => !i.pid)" 
            :key="index" 
            :config="item" 
        />
        <ConfirmBox></ConfirmBox>
    </div>
</template>

<script>
import { getStyle, getCanvasStyle } from '@/utils/style';
import localforage from 'localforage';
import ComponentWrapper from './ComponentWrapper';
import ConfirmBox from '@/components/ConfirmBox.vue';
import { changeStyleWithScale } from '@/utils/translate';
import { toPng } from 'html-to-image';
import { rootStore } from '@/stores/rootStore';
import { watch } from 'vue';
import { getValueByDotKey } from '@/utils/utils'
import { useGlobalUtils } from '@/hooks/useGlobalUtils';
import { excuteJsAction } from '@/hooks/useEventCentre';

const { initFilePath } = useGlobalUtils();
export default {
    components: { ComponentWrapper, ConfirmBox },
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
            rootStore.dataConfig.watchRegisters.forEach(({state, action}) => {
                watch(() => {
                    return getValueByDotKey(rootStore.dataConfig.stateSet, state.join('.'))
                }, (value) => {
                    excuteJsAction(action, {
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
