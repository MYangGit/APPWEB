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
                legend: {
                    layout: {
                        type: 'float',
                        value: 'rightTop',
                    },
                },
                series: [
                    {
                        type: 'gauge',
                        animationDuration: 1,
                        animationDurationUpdate: 1,
                        startAngle: this.propValue.startAngle,
                        endAngle: this.propValue.endAngle,
                        min: this.propValue.min,
                        max: this.propValue.max,
                        progress: {
                            show: this.propValue.isShowProgress,
                            width: 18,
                            itemStyle: {
                                color: '#5470c6',
                            },
                        },
                        pointer: {
                            itemStyle: {
                                color: '#5470c6',
                            },
                        },
                        axisLine: {
                            lineStyle: {
                                width: 18,
                            },
                        },
                        axisTick: {
                            show: this.propValue.isShowTick,
                        },
                        splitLine: {
                            length: 15,
                            lineStyle: {
                                width: 2,
                                color: '#999',
                            },
                        },
                        axisLabel: {
                            distance: 25,
                            color: this.propValue.labelColor,
                            fontSize: this.propValue.labelFontSize,
                        },
                        anchor: {
                            show: true,
                            showAbove: true,
                            size: 25,
                            itemStyle: {
                                borderWidth: 10,
                                borderColor: '#5470c6',
                            },
                        },
                        title: {
                            show: false,
                        },
                        detail: {
                            valueAnimation: true,
                            fontSize: this.propValue.valueFontSize,
                            color: this.propValue.valueColor,
                            formatter: `{value} ${this.propValue.valueUnit}`,
                            offsetCenter: [0, '70%'],
                        },
                        data: [
                            {
                                value: 70,
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
                this.options.series[0].startAngle = this.propValue.startAngle;
                this.options.series[0].endAngle = this.propValue.endAngle;
                this.options.series[0].min = this.propValue.min;
                this.options.series[0].max = this.propValue.max;
                this.options.series[0].progress.show = this.propValue.isShowProgress;
                this.options.series[0].axisTick.show = this.propValue.isShowTick;
                this.options.series[0].axisLabel.fontSize = this.propValue.labelFontSize;
                this.options.series[0].axisLabel.color = this.propValue.labelColor;
                this.options.series[0].detail.fontSize = this.propValue.valueFontSize;
                this.options.series[0].detail.color = this.propValue.valueColor;
                this.options.series[0].detail.name = this.propValue.name;
                this.options.series[0].detail.formatter = `{value} ${this.propValue.valueUnit}`;
                this.options.series[0].data = this.options.series[0].data.map((i) => ({
                    ...i,
                    value: parseFloat(i.value).toFixed(this.propValue.floatUnit),
                }));
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
            this.options.series[0].data = params
                .filter((i) => this.request.data.includes(i.name))
                .map((i) => ({
                    ...i,
                    value: parseFloat(i.value).toFixed(this.propValue.floatUnit),
                }));
            if (
                this.options.series[0].data.length &&
                this.options.series[0].data[0].value > this.propValue.warningValue &&
                this.propValue.warningValue
            ) {
                this.options.series[0].progress.itemStyle.color = '#ee6666';
                this.options.series[0].pointer.itemStyle.color = '#ee6666';
                this.options.series[0].anchor.itemStyle.borderColor = '#ee6666';
                this.options.series[0].detail.color = '#ee6666';
            } else {
                this.options.series[0].progress.itemStyle.color = '#5470c6';
                this.options.series[0].pointer.itemStyle.color = '#5470c6';
                this.options.series[0].anchor.itemStyle.borderColor = '#5470c6';
                this.options.series[0].detail.color = this.propValue.valueColor;
            }
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
