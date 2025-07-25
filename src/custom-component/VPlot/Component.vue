<template>
    <div>
        <div style="width: 100%;height: 100%;" id="chart"></div>
    </div>
</template>

<script>
import { getComputedGet } from '../../utils/utils'
import { rootStore } from '@/stores/rootStore';
import Plotly from 'plotly.js-dist-min';

export default {
    props: {
        propValue: {
            type: Object,
            default: () => ({
                value: '',
                options: [],
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    data () {
        return {
            resizeTimer: null
        }
    },
    computed: {
        lineDatas: {
            get() {
                return getComputedGet('lineDatas', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue) || []
            }
        },
    },
    methods: {
        getLineData() {
            let lineList = []
            this.lineDatas.forEach((item) => {
                lineList.push({
                    name: item.name,
                    x: item.x,
                    y: item.y,
                    hoverinfo: 'x+y',
                    type: 'scatter',
                    line: {
                        width: 1,
                        color: '#ffffff'
                    }
                })
            })
            return lineList
        },
        renderChart() {
            let dom = document.querySelector('#chart')
            if (!dom) return
            dom.innerHTML = ''
            let width = dom.offsetWidth
            let height = dom.offsetHeight
            let data = this.getLineData()
            let layout = {
                // 黑色
                plot_bgcolor: '#000000',
                paper_bgcolor: '#000000',
                width,
                height,
                xaxis: {
                    zeroline: false,
                    showline: true,
                    mirror: true,
                    // 白色字体
                    tickfont: {
                        color: '#ffffff',
                        size: 9
                    },
                },
                yaxis: {
                    gridcolor: '#374151', // 设置网格线颜色
                    gridwidth: 1, // 设置网格线宽度
                    griddash: 'dot',
                    tickfont: {
                        size: 9,
                        color: '#ffffff'
                    },
                    zeroline: false,
                    showline: true,
                    mirror: true
                },
                legend: {
                    xanchor: 'right',
                    x: 0.99,
                    y: 0.98,
                    bgcolor: '#000000',
                    bordercolor: '#cccccc',
                    // 字体白色
                    font: {
                        color: '#ffffff',
                        size: 10
                    },
                    borderwidth: 1,
                    traceorder: 'normal'
                },
                margin: {
                    l: 20,
                    r: 20,
                    b: 20,
                    t: 30
                },
                showlegend: true,
                showline: true
            };
            Plotly.newPlot('chart', data, layout, {
                responsive: true,
                scrollZoom: true,
            });
        }
    },
    mounted() {
        const targetDiv = document.getElementById('chart');
        if(!targetDiv) return;
        const observer = new ResizeObserver(entries => {
            clearTimeout(this.resizeTimer);
            this.resizeTimer = setTimeout(() => {
                this.renderChart()
            }, 200);
        });
        observer?.observe(targetDiv);
    },
    watch: {
        lineDatas: {
            handler() {
                this.renderChart()
            },
            deep: true,
        },
    },
}
</script>

<style lang="less" scoped>
</style>
