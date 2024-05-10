<template>
    <div>
        <erPlot
            style="width: 100%; height: 100%; display: block;"
            :dataSource="dataSource"
            :layout="layout"
        />
    </div>
</template>

<script>
import { getComputedGet } from '../../../utils/utils'
import { rootStore } from '@/stores/rootStore';

export default {
    props: {
        propValue: {
            type: Object,
            default: () => ({
                dataSource: [],
                layout: {},
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
        dataSource: {
            get () {
                return getComputedGet('dataSource', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue) || []
            }
        },
        layout: {
            get () {
                return getComputedGet('layout', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue) || []
            }
        },
    },
    mounted() {
        // const targetDiv = document.getElementById('chart');
        // const observer = new ResizeObserver(entries => {
        //     clearTimeout(this.resizeTimer);
        //     this.resizeTimer = setTimeout(() => {
        //         this.renderChart()
        //     }, 200);
        // });
        // observer.observe(targetDiv);
    }
}
</script>

<style lang="less" scoped>
</style>
