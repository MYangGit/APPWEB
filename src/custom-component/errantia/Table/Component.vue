<template>
    <div class="input-wrap">
        <erTable
            :borders="propValue.showBorder"
            :activeClickRow="propValue.activeClickRow"
            @onClickRow="handleClickRow"
            :outStyleHeader="{position: 'sticky', top: '0px'}"
            :columns="columns"
            :dataSource="dataSource"
        />
    </div>
</template>

<script>
import eventBus from '@/utils/eventBus';
import OnEvent from '../../common/OnEvent'
import { getComputedGet, getComputedSet } from '../../../utils/utils'
import { rootStore } from '@/stores/rootStore';
import { erTable } from 'errantia';

export default {
    extends: OnEvent,
    components: {
        erTable
    },
    props: {
        propValue: {
            type: Object,
            default: () => ({
                showBorder: false,
                activeClickRow: false,
                columns: [],
                dataSource: [],
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    methods: {
        handleClickRow(e, row, index) {
            let { onClickRow } = this.element.actionBinds;
            if (!onClickRow) return
            let fn = new Function(`return ${rootStore.dataConfig.actionSet[onClickRow]}`)()
            fn(rootStore.dataConfig.stateSet, e, row, index)
        }
    },
    computed: {
        columns () {
            return getComputedGet('columns', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
        },
        dataSource () {
            return getComputedGet('dataSource', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
        }
    },
    watch: {
        propValue: {
            handler(val) {
                const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'updateValue');
                if (linkageEvents.length) {
                    eventBus.$emit('updateValue', linkageEvents, { ...val });
                }
            },
            deep: true,
            immediate: true,
        },
    },
}
</script>

<style lang="less" scoped>
.input-wrap {
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    overflow-y: auto;
}
</style>