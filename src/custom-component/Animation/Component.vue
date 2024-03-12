<template>
    <div class="no-position">
        <TyAnimation v-if="update" ref="animation" :data="aniData" :model-info="modelInfo"></TyAnimation>
        <!-- <div id="modelEditor" class="moEditor"></div> -->
    </div>
</template>

<script>
import { mapState } from 'vuex';
import request from '@/utils/request';
import OnEvent from '../common/OnEvent';

export default {
    name: 'Animation',
    extends: OnEvent,
    props: {
        propValue: {
            type: Object,
            default: () => {},
        },
        request: {
            type: Object,
            default: () => {},
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    data() {
        return {
            /* eslint-disable */
            modelInfo: '',
            aniData: {},
            update: false,
        };
    },
    computed: mapState(['canvasStyleData']),
    watch: {},
    mounted() {
        if (this.canvasStyleData.simulationTaskId) {
            this.updateData({
                simulationTaskId: this.canvasStyleData.simulationTaskId,
            });
        }
    },
    methods: {
        updateData(params) {
            this.update = false;
            const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
            this.aniData = {
                taskId: params.simulationTaskId,
                speed: 1,
                name: userInfo.name,
                host: this.canvasStyleData.metaData.hostLocation
            };
            request({
                url: this.aniData.host + '/alchemy/web3d/getModelInfo',
                method: this.request.method || 'POST',
                data: {
                    taskId: this.aniData.taskId,
                    userName: userInfo.name
                },
            }).then(res => {
                this.modelInfo = res.data.data;
                this.update = true;
            })
        },
        play() {
            this.$refs.animation.animationPlay();
        },
        pause() {
            this.$refs.animation.animationPause();
        },
        reset() {
            this.$refs.animation.animationReset();
        }
    },
};
</script>

<style lang="less" scoped>
.moEditor {
    width: 100%;
    height: 100%;
    position: relative;
}
</style>
