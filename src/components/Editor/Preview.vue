<template>
    <div ref="container" class="bg preview">
        <!-- <el-button v-if="!isScreenshot" class="close" @click="close">关闭</el-button> -->
        <el-button v-if="isScreenshot" class="close" @click="htmlToImage">确定</el-button>
        <div class="canvas-container">
            <div
                v-loading="loading"
                class="canvas"
                :style="{
                    ...getCanvasStyle(canvasStyleData),
                    width: changeStyleWithScale(canvasStyleData.width) + 'px',
                    height: changeStyleWithScale(canvasStyleData.height) + 'px',
                }"
            >
                <ComponentWrapper v-for="(item, index) in copyData.filter((i) => !i.pid)" :key="index" :config="item" />
            </div>
            
        </div>
    </div>
</template>

<script>
import { getStyle, getCanvasStyle } from '@/utils/style';
import localforage from 'localforage';
import ComponentWrapper from './ComponentWrapper';
import { changeStyleWithScale } from '@/utils/translate';
import { toPng } from 'html-to-image';

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
            heatTimer: null,
            loading: false,
        };
    },
    created() {
        localforage.getItem('canvasData').then((data) => {
            this.copyData = JSON.parse(data) || []
        });
        localforage.getItem('canvasStyle').then((data) => {
            this.canvasStyleData = JSON.parse(data);
        });
    },
    methods: {
        getStyle,
        getCanvasStyle,
        changeStyleWithScale,

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
        }
    },
};
</script>

<style lang="less" scoped>
.bg {
    width: 100%;
    height: 100%;
    position: fixed;
    background: rgb(0, 0, 0, 0.5);
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
