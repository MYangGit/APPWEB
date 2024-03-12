<template>
    <div class="no-position" style="position: relative;">
        <el-button v-show="propValue.showPlay" class="auto-play" @click="autoPlay">开始播放</el-button>
        <TyChart v-if="update" :id="id" :options="options" @ready="ready"></TyChart>
    </div>
</template>

<script>
import { mapState } from 'vuex';
import elementResize from 'element-resize-detector';
import request from '@/utils/request';
import eventBus from '@/utils/eventBus';
import { createUuid } from '@/utils/utils';
import OnEvent from '../common/OnEvent';
import { i } from 'mathjs';

export default {
    name: 'TyCharts',
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
            id: createUuid(),
            options: {
                title: {
                    text: this.propValue.title,
                    textStyle: {
                        color: this.propValue.titleColor,
                        fontSize: this.propValue.titleSize,
                    },
                    left: this.propValue.titleAlign,
                },
                legend: {
                    layout: {
                        type: 'float',
                        value: 'rightTop',
                    },
                    data: [],
                },
                xAxis: {
                    type: 'category',
                    data: ['1', '2', '3', '4', '5', '6', '7'],
                },
                yAxis: {
                    type: 'value',
                },
                tooltip: {
                    trigger: 'axis',
                    showContent: false,
                },
                series: [
                    {
                        data: [150, 230, 224, 218, 135, 147, 260],
                        type: this.propValue.props.type,
                        smooth: true,
                        lineStyle: {
                            color: '#5470c6',
                            type: 'solid',
                            width: 2,
                        },
                        legendAttr: {
                            default: 'mLoad',
                            name: 'mLoad',
                            tempName: 'mLoad',
                        },
                    },
                ],
            },
            colors: [
                // 默认的颜色数组
                '#5470c6',
                '#91cc75',
                '#fac858',
                '#ee6666',
                '#73c0de',
                '#3ba272',
                '#fc8452',
                '#9a60b4',
                '#ea7ccc',
            ],
            update: true,
            myChart: null,
            timer: null,
        };
    },
    computed: {
        ...mapState(['canvasStyleData']),
    },
    watch: {
        request: {
            handler() {
                if (this.request.url && this.request.method && this.request.data.length) {
                    this.updateData({});
                }
            },
            deep: true,
        },
        propValue: {
            handler() {
                this.options.title.text = this.propValue.title;
                this.options.title.textStyle.color = this.propValue.titleColor;
                this.options.title.textStyle.fontSize = this.propValue.titleSize;
                this.options.title.left = this.propValue.titleAlign;
                this.options.series = this.options.series.map(i => ({ ...i, type: this.propValue.props.type }));
                if (this.myChart) {
                    this.myChart.setOption(this.options);
                }
                if (this.propValue.autoPlay) {
                    if (this.timer) {
                        window.clearInterval(this.timer);
                        this.timer = null;
                    }
                    this.autoPlay();
                } else if (this.timer) {
                    window.clearInterval(this.timer);
                    this.timer = null;
                }
            },
            deep: true,
        },
    },
    mounted() {
        const elementResizeObj = elementResize({
            strategy: 'scroll', // <- 推荐监听滚动，提升性能
            callOnAdd: true, // 添加侦听器时是否应调用,默认true
        });
        elementResizeObj.listenTo(document.getElementById(this.id), (element) => {
            if (this.myChart) this.myChart.resize();
        });
        if (this.canvasStyleData.simulationTaskId) {
            this.updateData({
                simulationTaskId: this.canvasStyleData.simulationTaskId,
            });
        }
    },
    beforeDestroy() {
        if (this.timer) {
            window.clearInterval(this.timer);
            this.timer = null;
        }
    },
    methods: {
        ready(myChart) {
            this.myChart = myChart;
            this.myChart.on('updateAxisPointer', (params) => {
                if (params.dataIndex) {
                    const indexData = this.options.series.map((i) => ({
                        name: i.legendAttr.default,
                        value: i.data[params.dataIndex],
                    }));
                    const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'updateAxisPointer');
                    if (linkageEvents.length) {
                        eventBus.$emit('updateAxisPointer', linkageEvents, indexData);
                    }
                }
            });
        },
        autoPlay() {
            if (!this.timer) {
                let index = 0;
                this.timer = setInterval(() => {
                    if (index < this.options.xAxis.data.length) {
                        index++;
                    } else if (!this.propValue.circulate) {
                        window.clearInterval(this.timer);
                        this.timer = null;
                    } else {
                        index = 0;
                    }
                    this.myChart.dispatchAction({
                        type: 'updateAxisPointer',
                        seriesIndex: 0,
                        dataIndex: index,
                    });
                }, this.propValue.autoPlayTime || 100);
            }
        },
        setParams(params) {
            this.request.data = params;
        },
        updateData(params) {
            const variableName = this.request.data.filter((i) => i[0] === 'variableName');
            this.loadData(params).then((res) => {
                if (this.request.data && this.request.data.length && variableName.length) {
                    this.options.legend.data = variableName.map((i) => i[1]);
                    this.options.xAxis.data = res[0].data.data.time;
                    this.options.series = variableName
                        .map((i) => i[1])
                        .map((i, ind) => ({
                            data: res[ind].data.data.values,
                            type: this.propValue.props.type,
                            smooth: true,
                            lineStyle: {
                                color: this.colors[ind % 9],
                                type: 'solid',
                                width: 2,
                            },
                            legendAttr: {
                                default: i,
                                name: i,
                                tempName: i,
                            },
                        }));
                } else {
                    this.options.series[0].data = res.data.data.values;
                    this.options.xAxis.data = res.data.data.time;
                    this.options.series[0].legendAttr = {
                        default: params.path,
                        name: params.path,
                        tempName: params.path,
                    };
                }
                // this.update = false;
                // this.$nextTick(() => {
                //     this.update = true;
                //     if (this.myChart) this.myChart.resize();
                // });
                if (this.myChart) this.myChart.setOption(this.options);
                if (this.propValue.autoPlay) this.autoPlay();
            });
        },
        loadData(params) {
            const variableName = this.request.data.filter((i) => i[0] === 'variableName');
            const taskId = this.request.data.filter((i) => i[0] === 'taskId');
            const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
            if (this.request.data && this.request.data.length && variableName.length) {
                const requests = [];
                variableName
                    .map((i) => i[1])
                    .forEach((i) => {
                        const http = request({
                            url: this.request.url,
                            method: this.request.method,
                            params: {
                                userName: userInfo.name || '',
                            },
                            data: {
                                factors: [],
                                operator: '',
                                simulationTaskId: params.simulationTaskId || (taskId.length ? taskId[0][1] : '') || this.canvasStyleData.simulationTaskId,
                                variableName: i,
                            },
                        });
                        requests.push(http);
                    });
                return Promise.all(requests);
            }
            return request({
                url: this.request.url,
                method: this.request.method,
                params: {
                    userName: userInfo.name || '',
                },
                data: {
                    factors: [],
                    operator: '',
                    simulationTaskId: params.simulationTaskId || (taskId.length ? taskId[0][1] : '') || this.canvasStyleData.simulationTaskId,
                    variableName: params.path,
                },
            });
        },
    },
};
</script>

<style lang="less" scoped>
.auto-play {
    position: absolute;
    top: 0px;
    left: 0px;
    z-index: 222;
}
</style>
