<template>
    <div class="input-wrap">
        <erTable
            :style="{'text-align': propValue.textAlign}"
            :borders="propValue.showBorder"
            :activeClickRow="propValue.activeClickRow"
            @onContextMenuRow="handleContextMenuRow"
            @onDbClickRow="handleDbClickRow"
            @onClickRow="handleClickRow"
            :outStyleHeader="{position: 'sticky', top: '0px'}"
            :columns="columns"
            :dataSource="dataSource"
        >   <template v-if="showOperate" v-slot:operate="{ row, index }">
                <el-icon><Delete @click.stop="handleDelete(row, index)" /></el-icon>
                <el-icon style="margin-left: 10px;"><Setting /></el-icon>
            </template>
            <template v-if="serialNumber" v-slot:serialNumber="{ index, row }">
               <el-checkbox v-if="row?.checkbox !== undefined" v-model="row.checkbox" />
               <span v-else>{{ index }}</span>
            </template>
            <template v-slot:name="{ row, index, column }">
                <input 
                    v-if="reName == row.name"
                    @blur="handNameBlur(row, index)" 
                    style="width: 100%;" 
                    type="text"
                    v-model="newName"
                >
                <div v-else :class="{'active-row': row?.uuid === currUuid}">
                    <el-tooltip
                        effect="dark"
                        :content="row.name"
                        placement="bottom"
                    >
                       <div                 
                          class="nameText" 
                          :style="{ width: `${column.width}px` }" 
                        >
                           {{ row.name }} 
                       </div> 
                    </el-tooltip>
                </div>
            </template>
        </erTable>
    </div>
</template>

<script>
import Container from '../../common/Container.vue';
import PreviewContainer from '../../common/PreviewContainer.vue';
import { getComputedGet, getComputedSet, isEmpty } from '../../../utils/utils'
import { rootStore } from '@/stores/rootStore';
import { erTable } from 'errantia';
import { useEventCentre } from '@/hooks/useEventCentre';

const { onClickOther } = useEventCentre();
export default {
    components: {
        erTable,
        Container,
        PreviewContainer,
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
                reName: '',
                newName: '',
                currUuid: '',
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    methods: {
        handNameBlur(row, index) {
            onClickOther({element: this.element, clickName: 'onNameBlur', params: { newName: this.newName, row, index}})
            this.reName = ''
            if(isEmpty(this.newName)) return
            this.dataSource[index].name = this.newName
        },
        handleClickRow(e, row, index) {
            onClickOther({element: this.element, clickName:'onClickRow', params: { e, row, index } })
        },
        handleDbClickRow(e, row, index, col, colIndex) {
            this.reName = row.name
            this.newName = row.name
            onClickOther({element: this.element, clickName:'onDbClickRow', params: { e, row, index, col, colIndex } })
        },
        handleContextMenuRow(e, row, index) {
            onClickOther({element: this.element, clickName:'onContextMenuRow', params: { e, row, index } })
        },
        handleDelete(row, index) {
            onClickOther({element: this.element, clickName:'onClickDelete', params: { row, index } })
        }
    },
    computed: {
        newName: {
            get() {
                return getComputedGet('newName', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('newName', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        reName: {
            get() {
                return getComputedGet('reName', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('reName', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        currUuid: {
            get() {
                return getComputedGet('currUuid', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('currUuid', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        serialNumber () {
            return getComputedGet('serialNumber', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
        },
        showOperate () {
            return getComputedGet('showOperate', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
        },
        columns : {
            get() {
                return getComputedGet('columns', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('columns', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        dataSource: {
            get() {
                return getComputedGet('dataSource', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('dataSource', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
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
.nameText {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.active-row {
    background-color: #dee2e6;
    margin: -5px;
    padding: 5px;
    &:hover {
        background-color: #e9ecef;
    }
}
</style>