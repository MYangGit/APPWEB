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
import { mapState } from 'vuex';
import localforage from 'localforage';
import Cookies from 'js-cookie';
import ComponentWrapper from './ComponentWrapper';
import { changeStyleWithScale } from '@/utils/translate';
import { toPng } from 'html-to-image';
import { deepCopy, createUuid, getQueryVariable } from '@/utils/utils';
import { initWebSocket, initServer, initProject, loadModel, loadLibrary } from '@/utils/websocket';
import request from '@/utils/request';
import eventBus from '@/utils/eventBus';

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
            pageKey: createUuid(),
            heatTimer: null,
            loading: false,
        };
    },
    computed: mapState(['componentData', 'canvasStyleData', 'projectData']),
    created() {
        this.$store.commit('setEditMode', 'preview');
        // if (localStorage.getItem('canvasData')) {
        //     this.$store.commit('setComponentData', JSON.parse(localStorage.getItem('canvasData')));
        // }

        // if (localStorage.getItem('canvasStyle')) {
        //     this.$store.commit('setCanvasStyle', JSON.parse(localStorage.getItem('canvasStyle')));
        // }
        if (getQueryVariable('repoId')) {
            this.getAppDetail();
        } else {
            localforage.getItem('canvasData', (err, value) => {
                if (value) {
                    this.$store.commit('setComponentData', JSON.parse(value));
                }
                localforage.getItem('canvasStyle', (err, value) => {
                    if (value) {
                        this.$store.commit('setCanvasStyle', JSON.parse(value));
                        this.$set(this, 'copyData', deepCopy(this.componentData));
                        if (this.canvasStyleData.projectId) {
                            // this.getRunningDockerByUser();
                            this.getDetail();
                        }
                    }
                });
            });
        }
        // this.$set(this, 'copyData', deepCopy(this.componentData));
        // if (this.canvasStyleData.projectId) {
        //     // this.getRunningDockerByUser();
        //     this.getDetail();
        // }
        // this.getAppDetail();
        eventBus.$on('updateList', () => {
            if (this.canvasStyleData.projectId) {
                // this.getRunningDockerByUser();
                this.getDetail();
            }
        });
        eventBus.$on('changeModel', () => {
            if (this.canvasStyleData.projectId) {
                // this.getRunningDockerByUser();
                this.getDetail();
            }
        });
    },
    beforeDestroy() {
        if (this.heatTimer) {
            window.clearInterval(this.heatTimer);
        }
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
        },

        getDetail() {
            request({
                url: '/mohub/public/repo/detail',
                method: 'GET',
                params: { projectId: this.canvasStyleData.projectId },
            }).then((res) => {
                this.$store.commit('setProjectData', { ...res.data.data, editable: true });
            });
        },

        getAppDetail() {
            const params = window.location.href.split('?');
            if (params.length > 1) {
                request({
                    url: `/mohub/tgit/getFileContent?${params[1]}`,
                    method: 'GET',
                }).then((res) => {
                    const appData = JSON.parse(res.data.data);
                    if (appData.componentData) {
                        this.$store.commit('setComponentData', appData.componentData);
                    }
                    if (appData.canvasStyleData) {
                        this.$store.commit('setCanvasStyle', appData.canvasStyleData);
                    }
                    this.$set(this, 'copyData', deepCopy(appData.componentData));
                    if (appData.canvasStyleData.projectId) {
                        // this.getRunningDockerByUser();
                        this.getDetail();
                    }
                });
            }
        },

        // 建立websocket连接
        createWebsocket(url) {
            setTimeout(() => {
                initWebSocket(url).then((websocket) => {
                    this.websocket = websocket;
                    this.getServiceInfo();
                });
            }, 10);
        },
        getRunningDockerByUser() {
            this.loading = true;
            return request({
                url: '/mohub/docker/getRunningDockerByUser',
                method: 'GET',
            }).then((res) => {
                if (res.data.data?.pageKey) {
                    request({
                        url: '/mohub/docker/deleteDocker',
                        method: 'GET',
                        params: { pageKey: res.data.data.pageKey },
                    }).then(() => {
                        this.initDocker();
                    });
                } else {
                    this.initDocker();
                }
            });
        },
        initDocker() {
            request({
                url: '/mohub/docker/initDockerByPageKey',
                method: 'GET',
                params: { pageKey: this.pageKey },
            });
            let timer = setInterval(() => {
                this.queryDocker(timer);
            }, 1000);
            this.heatTimer = setInterval(() => {
                this.sendHead();
            }, 3000);
        },

        queryDocker(timer) {
            request({
                url: '/mohub/docker/getDockerByPageKey',
                method: 'GET',
                params: { pageKey: this.pageKey },
            }).then((res) => {
                if (res.data.code == 0 && res.data.data.status == 'RUNNING') {
                    window.clearInterval(timer);
                    this.createWebsocket(res.data.data.websocketAddress);
                }
            });
        },

        sendHead() {
            request({
                url: '/mohub/docker/sendHeartbeat',
                method: 'GET',
                params: { pageKey: this.pageKey },
            });
        },

        getServiceInfo() {
            request({
                url: '/mohub/user/queryServerInfo',
                method: 'GET',
            }).then((res) => {
                if (res.data.code == 0 && res.data.data) {
                    const host = res.data.data.split(':');
                    let request = {
                        ipAddress: host[0],
                        port: host[1],
                        token: Cookies.get('token_mohub'),
                    };
                    initServer(request).then(() => {
                        const params = {
                            projectId: this.canvasStyleData.projectId,
                            projectType: 'development',
                        };
                        initProject(params).then(() => {
                            loadModel(params).then(() => {
                                loadLibrary({
                                    libraryName: 'Modelica',
                                    libraryVersion: '4.0',
                                    // libraryVersion: '3.2.3'
                                }).then(() => {
                                    eventBus.$emit('connected');
                                    this.loading = false;
                                });
                            });
                        });
                    });
                }
            });
        },
    },
};
</script>

<style lang=less scoped>
.bg {
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    position: fixed;
    background: rgb(0, 0, 0, 0.5);
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: auto;
    padding: 20px;

    .canvas-container {
        // width: calc(100% - 40px);
        // height: calc(100% - 40px);
        // overflow: auto;

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
