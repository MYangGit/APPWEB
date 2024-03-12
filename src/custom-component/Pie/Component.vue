<template>
    <div class="no-position">
        <div :id="id" style="height: 100%"></div>
    </div>
</template>

<script>
import * as echarts from 'echarts';
import elementResize from 'element-resize-detector';
import request from '@/utils/request';
import { createUuid } from '@/utils/utils';
import OnEvent from '../common/OnEvent';

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
                series: [
                    {
                        name: 'Access From',
                        type: 'pie',
                        radius: '50%',
                        data: [
                            { value: 1048, name: 'Search Engine' },
                            { value: 735, name: 'Direct' },
                            { value: 580, name: 'Email' },
                            { value: 484, name: 'Union Ads' },
                            { value: 300, name: 'Video Ads' },
                        ],
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)',
                            },
                        },
                    },
                ],
            },
            update: true,
        };
    },
    watch: {
        propValue: {
            handler() {
                this.options.title.text = this.propValue.title;
                this.options.title.textStyle.color = this.propValue.titleColor;
                this.options.title.textStyle.fontSize = this.propValue.titleSize;
                this.options.title.left = this.propValue.titleAlign;
                if (this.myChart) {
                    this.myChart.setOption(this.options);
                }
            },
            deep: true,
        },
    },
    mounted() {
        this.$nextTick(() => {
            this.initChart();
        });
    },
    methods: {
        initChart() {
            this.myChart = echarts.init(document.getElementById(this.id));
            this.myChart.setOption(this.options);
            const elementResizeObj = elementResize({
                strategy: 'scroll', // <- 推荐监听滚动，提升性能
                callOnAdd: true, // 添加侦听器时是否应调用,默认true
            });
            elementResizeObj.listenTo(document.getElementById(this.id), (element) => {
                this.myChart.resize(); // 当元素尺寸发生改变是会触发此事件，刷新图表
            });
        },
        updateData(params) {
            // eslint-disable-next-line arrow-body-style
            this.options.series[0].data = params.filter((i) => {
                return this.request.data.includes(i.name);
            });
            if (this.myChart) {
                this.myChart.setOption(this.options);
            }
        },
        loadData(params) {
            const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
            return request({
                url: this.request.url,
                method: this.request.method,
                params: {
                    userName: userInfo.name,
                },
                data: {
                    factors: [],
                    operator: '',
                    simulationTaskId: params.simulationTaskId,
                    variableName: params.path,
                },
            });
        },
    },
};
</script>

<style lang="less" scoped></style>
