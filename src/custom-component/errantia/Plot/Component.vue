<template>
   <div>
    <erPlot
        style="width: 100%; height: 100%; display: flex;"
        v-size-ob="handleResize"
        :id="propValue.domId"
        :dataSource="dataSource"
        :layout="layout"
    />
   </div>
</template>

<script>
import { getComputedGet, getComputedSet} from '../../../utils/utils'
import { rootStore } from '@/stores/rootStore';

export default {
    props: {
        propValue: {
            type: Object,
            default: () => ({
                dataSource: [],
                layout: {},
                domId: 'chartPlot',
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    data () {
        return {
            resizeTimer: null,
            dataSourceTrue: [],
        }
    },
    computed: {
        dataSource: {
            get () {
                return getComputedGet('dataSource', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue) || []
            },
            set(val) {
                getComputedSet('dataSource', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        layout: {
            get () {
                return getComputedGet('layout', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue) || []
            }
        },
    },
    methods: {
        renderChart() {
            let tempData = this.dataSource
            this.dataSource = []
            this.$nextTick(() => {
                this.dataSource = tempData
            })
        },
        handleResize() {
            this.renderChart()
        }
    },
}
</script>

<style lang="less" scoped>
</style>
