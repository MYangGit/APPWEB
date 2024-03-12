<template>
    <div class="no-position">
        <el-button @click="startSimu">开始仿真</el-button>

        <el-dialog
            title="仿真设置"
            :visible.sync="dialogVisible"
            width="30%"
            :before-close="handleClose"
            :append-to-body="true"
            class="attribute-dialog"
        >
            <TyModelAttributes
                v-loading="loading"
                :project-data="projectData"
                :algorithms="algorithms"
                @updateSimulateData="updateSimulateData"
            ></TyModelAttributes>
        </el-dialog>
    </div>
</template>

<script>
import { mapState } from 'vuex';
import { deepCopy } from '@/utils/utils';
import eventBus from '@/utils/eventBus';
import request from '@/utils/request';
import { Loading } from 'element-ui';
import OnEvent from '../common/OnEvent';

export default {
    name: 'ModelAttributes',
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
            dialogVisible: false,
            modelInfo: {},
            loading: false,
            params: {},
            algorithms: [
                {
                    label: 'Dassl',
                    value: 'Dassl',
                },
                {
                    label: 'Radau5',
                    value: 'Radau5',
                },
                {
                    label: 'Dop853',
                    value: 'Dop853',
                },
                {
                    label: 'Dopri5',
                    value: 'Dopri5',
                },
                {
                    label: 'Mebdfdae',
                    value: 'Mebdfdae',
                },
                {
                    label: 'Mebdfi',
                    value: 'Mebdfi',
                },
                {
                    label: 'Dlsode',
                    value: 'Dlsode',
                },
                {
                    label: 'Dlsodar',
                    value: 'Dlsodar',
                },
                {
                    label: 'Cvode',
                    value: 'Cvode',
                },
                {
                    label: 'Ida',
                    value: 'Ida',
                },
                {
                    label: 'Sdirk34',
                    value: 'Sdirk34',
                },
                {
                    label: 'Esdirk23',
                    value: 'Esdirk23',
                },
                {
                    label: 'Esdirk34',
                    value: 'Esdirk34',
                },
                {
                    label: 'Esdirk45',
                    value: 'Esdirk45',
                },
                {
                    label: 'Euler',
                    value: 'Euler',
                },
                {
                    label: 'ModifiedEuler',
                    value: 'ModifiedEuler',
                },
                {
                    label: 'Rkfix2',
                    value: 'Rkfix2',
                },
                {
                    label: 'Rkfix3',
                    value: 'Rkfix3',
                },
                {
                    label: 'Rkfix4',
                    value: 'Rkfix4',
                },
                {
                    label: 'Rkfix6',
                    value: 'Rkfix6',
                },
                {
                    label: 'Rkfix8',
                    value: 'Rkfix8',
                },
            ],
        };
    },
    computed: {
        ...mapState(['canvasStyleData', 'projectData']),
    },
    methods: {
        startSimu() {
            if (this.propValue.showSetting) {
                this.dialogVisible = true;
            } else {
                this.startSimulate({
                    algorithm: 'Dassl',
                    fixedOrInitStepSize: '',
                    intervalLength: 0.008,
                    numberOfIntervals: 500,
                    selectedIntervalLength: false,
                    startTime: 0,
                    stopTime: 1,
                    storeEventValue: false,
                    tolerance: 0.0001,
                });
            }
        },
        handleClose() {
            this.dialogVisible = false;
        },
        updateData(params) {
            this.modelInfo = params;
            console.log('仿真属性-刷新数据', params);
        },
        updateParams(params) {
            this.params[params.key] = params.value;
            console.log('仿真属性-刷新参数', this.params);
        },
        setParams(params) {
            this.params = params;
            console.log('仿真属性-设置参数', this.params);
        },
        updateSimulateData(params) {
            this.startSimulate(params);
        },
        isFixed(value) {
            const result = ['Euler', 'ModifiedEuler', 'Rkfix2', 'Rkfix3', 'Rkfix4', 'Rkfix6', 'Rkfix8'];
            return result.includes(value);
        },
        startSimulate(oldParams) {
            const params = deepCopy(oldParams);
            this.loading = true;
            let requestParams = {
                simulationAction: 'SIMULATE',
                modelFullName: this.canvasStyleData.metaData.fullName,
                setting: Object.assign(params, {
                    fixedOrInitStepSize: params.fixedOrInitStepSize === 'default' ? '' : params.fixedOrInitStepSize,
                }),
                params: this.params,
                repoId: this.projectData.repoId,
            };
            request({
                url: '/mohub/simulation/fireTask',
                method: 'POST',
                data: requestParams,
            }).then((res) => {
                if (res.data.data) {
                    this.creatTimer(res.data.data.id);
                } else {
                    this.loading = false;
                    this.$message.warning(res.data.message);
                }
            });
        },
        creatTimer(simulationTaskId) {
            const timer = setInterval(() => {
                this.querySimulationTask(simulationTaskId, timer);
            }, 1000);
        },
        querySimulationTask(simulationTaskId, timer) {
            let loadingInstance = Loading.service({ fullscreen: true, text: '配置仿真环境可能需要一会儿，请耐心等待' });
            request({
                url: '/mohub/simulation/task',
                method: 'POST',
                data: {
                    simulationTaskId,
                },
            }).then((res) => {
                if (res.data.data.status === 'SUCCEED') {
                    this.loading = false;
                    window.clearInterval(timer);
                    this.$nextTick(() => { // 以服务的方式调用的 Loading 需要异步关闭
                        loadingInstance.close();
                    });
                    this.canvasStyleData.simulationTaskId = simulationTaskId;
                    const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'simulateCompleted');
                    if (linkageEvents.length) {
                        eventBus.$emit('simulateCompleted', linkageEvents, { ...this.modelInfo, simulationTaskId });
                    }
                } else if (res.data.data.status === 'FAILED') {
                    this.loading = false;
                    window.clearInterval(timer);
                    this.$nextTick(() => { // 以服务的方式调用的 Loading 需要异步关闭
                        loadingInstance.close();
                    });
                    this.$message.warning('仿真失败');
                }
            });
        },
    },
};
</script>

<style lang="less" scoped>
.no-position {
    .el-dialog__body {
        height: 750px;
    }
}
</style>
