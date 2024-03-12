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
                radar: {
                    // shape: 'circle',
                    indicator: [
                        { name: 'Sales', max: 6500 },
                        { name: 'Administration', max: 16000 },
                        { name: 'Information Technology', max: 30000 },
                        { name: 'Customer Support', max: 38000 },
                        { name: 'Development', max: 52000 },
                        { name: 'Marketing', max: 25000 },
                    ],
                },
                series: [
                    {
                        name: 'Budget vs spending',
                        type: 'radar',
                        data: [
                            {
                                value: [4200, 3000, 20000, 35000, 50000, 18000],
                                name: 'Allocated Budget',
                            },
                        ],
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
            console.log(document.getElementById(this.id));
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
            this.options.radar.indicator = params.filter((i) => {
                return this.request.data.includes(i.name);
            });
            this.options.series[0].data[0].value = params
                // eslint-disable-next-line arrow-body-style
                .filter((i) => {
                    return this.request.data.includes(i.name);
                })
                .map((i) => i.value);
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
