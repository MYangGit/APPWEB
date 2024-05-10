<template>
    <div class="input-wrap">
        <erTable
            :style="{'text-align': propValue.textAlign}"
            :borders="propValue.showBorder"
            :activeClickRow="propValue.activeClickRow"
            @onClickRow="handleClickRow"
            :outStyleHeader="{position: 'sticky', top: '0px'}"
            :columns="columns"
            :dataSource="dataSource"
        >   <template v-if="showOperate" v-slot:operate="{ row, index }">
                <el-icon><Delete @click.stop="handleDelete(row, index)" /></el-icon>
            </template>
            <template v-if="serialNumber" v-slot:serialNumber="{ index }">
               <span>{{ index }}</span>
            </template>
        </erTable>
    </div>
</template>

<script>
import { getComputedGet } from '../../../utils/utils'
import { rootStore } from '@/stores/rootStore';
import { erTable } from 'errantia';
import { useEventCentre } from '@/hooks/useEventCentre';

const { onClickOther } = useEventCentre();
export default {
    components: {
        erTable
    },
    props: {
        propValue: {
            type: Object,
            default: () => ({
                showBorder: false,
                activeClickRow: false,
                showOperate: false,
                serialNumber: false,
                textAlign: 'left',
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
            onClickOther({element: this.element, clickName:'onClickRow', params: { e, row, index } })
        },
        handleDelete(row, index) {
            onClickOther({element: this.element, clickName:'onClickDelete', params: { row, index } })
        }
    },
    computed: {
        serialNumber () {
            return getComputedGet('serialNumber', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
        },
        showOperate () {
            return getComputedGet('showOperate', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
        },
        columns () {
            return getComputedGet('columns', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
        },
        dataSource () {
            return getComputedGet('dataSource', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
        }
    }
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