<template>
    <div class="input-wrap">
        <erTable
            :style="{'text-align': propValue.textAlign}"
            :borders="propValue.showBorder"
            :activeClickRow="propValue.activeClickRow"
            :outStyleHeader="{position: 'sticky', zIndex: 99, top: '0px',  ...(propValue.overflowWrap ? { overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'} : {})}" 
            :columns="visibleColumns"
            :dataSource="dataSource"
            :uuIdOnly="currUuid"
            :uuIdName="propValue.uuIdName"
            @onContextMenuRow="handleContextMenuRow"
            @onDbClickRow="handleDbClickRow"
            @onClickRow="handleClickRow"
        >   <template v-if="showOperate" v-slot:operate="{ row, index, column }">
                <erFlex justify="space-around" aligns="center" >
                    <el-icon title="删除" v-if="column['openOperate']?.includes('delete')"><Delete @click.stop="handleOperate(row, index, 'delete' )" /></el-icon>
                    <el-icon title="编辑" v-if="column['openOperate']?.includes('edit')"><Edit @click.stop="handleOperate(row, index, 'edit')" /></el-icon>
                    <el-icon title="暂停" v-if="column['openOperate']?.includes('pause')"><VideoPause @click.stop="handleOperate(row, index, 'pause')" /></el-icon>
                    <el-icon title="下载" v-if="column['openOperate']?.includes('download')"><Download @click.stop="handleOperate(row, index, 'download')" /></el-icon>
                    <el-icon title="查看" v-if="column['openOperate']?.includes('view')"><View @click.stop="handleOperate(row, index, 'view')" /></el-icon>
                    <el-icon title="保存" v-if="column['openOperate']?.includes('save')"><Folder @click.stop="handleOperate(row, index, 'save')" /></el-icon>
                </erFlex>
            </template>
            <template v-if="serialNumber" v-slot:serialNumber="{ index }">
               <span>{{ index }}</span>
            </template>
            <template v-slot:name="{ row, index, column }">
                <input 
                    v-if="reName == row[column.key]"
                    @blur="handNameBlur(row, index)" 
                    style="width: 100%;" 
                    type="text"
                    v-model="newName"
                >
                <div v-else>
                    <el-tooltip
                        effect="dark"
                        :content="row[column.key]"
                        placement="bottom"
                    >
                       <div                 
                          class="nameText" 
                          :style="{ width: `${column?.width}px` }" 
                        >
                           {{ row[column.key] }}
                       </div> 
                    </el-tooltip>
                </div>
            </template>
            <template v-slot:custom="{ row, index, column, colIdx }">
                <div @click.stop>
                    <el-checkbox 
                        v-if="column?.type === 'checkbox'" 
                        v-model="row[column.key]" 
                        @change="handleRowCheckbox(row, index, column)"
                    />
                    <el-input
                        v-else-if="column?.type === 'input'"
                        type="text"
                        :style="{ width: `${column?.width}px` }"
                        v-model="row[column.key]"
                        @paste.stop="handlePaste($event, index, colIdx)"
                    />
                    <el-select
                        v-else-if="column?.type === 'select'"
                        v-model="row[column.key]"
                        :style="{ width: `${column?.width}px` }"
                        @change="(newVal) => handleSelectChange(newVal, row, index, column)"
                    >
                        <template v-if="!isEmpty(column?.options)"  v-for="opt of column.options">
                            <el-option 
                                v-if="!isEmpty(opt.index)"
                                :label="`${opt.label}${opt.index}`" 
                                :value="opt.value" 
                            />
                            <el-option 
                                v-else
                                :label="opt.label" 
                                :value="opt.value" 
                            />
                        </template>
                    </el-select>
                    <div v-else-if="column?.type === 'table'" style="display: flex;">
                        <el-tooltip  
                            v-if="!isEmpty(row[column.key])"
                            effect="dark"
                            :content="`[${showTable(column, row[column.key])}]`"
                            placement="bottom"
                        >
                          <div :style="{ width: `${column?.width}px` }">{{ showTable(column, row[column.key]) }}</div>
                        </el-tooltip>
                    </div> 
                    <el-tooltip
                        v-else
                        effect="dark"
                        :content="row[column.key]"
                        placement="bottom"
                    >
                       <div class="nameText" :style="{ width: `${column?.width}px`, maxHeight: `300px` }"  >{{row[column.key]}}</div>
                   </el-tooltip>
                </div>
            </template> 
        </erTable>
        <div v-if="isEmpty(dataSource) && propValue.noDataHints" style="height: 100px; margin: 0 auto;">暂无数据</div>
    </div>
</template>

<script>
import Container from '../../common/Container.vue';
import PreviewContainer from '../../common/PreviewContainer.vue';
import { getComputedGet, getComputedSet, isEmpty, flattenArray, createUuid } from '../../../utils/utils'
import { rootStore } from '@/stores/rootStore';
import { erFlex, erTable } from 'errantia';
import { useEventCentre } from '@/hooks/useEventCentre';
import { useUtilsCentre}  from '@/hooks/useUtilsCentre';

const { onClickOther } = useEventCentre();
const { transformToValueArray } = useUtilsCentre();
export default {
    components: {
        erFlex,
        erTable,
        Container,
        PreviewContainer,
    },
    props: {
        propValue: {
            type: Object,
            default: () => ({
                noDataHints: false,
                overflowWrap: false,
                activateText: "",
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
                uuIdName: '',
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    methods: {
        isEmpty,
        flattenArray,
        showTable(column, data) {
            if (!isEmpty(column.config)) {
                column = JSON.parse(column.config)?.columns
            }
            data = JSON.parse(data)
            return flattenArray(transformToValueArray(column, data)) 
        },
        handTable(event, row, column) {
            event.stopPropagation()
            event.preventDefault()
            onClickOther({element: this.element, clickName:'onClickTable', params: { row, column, activateText: this.activateText} })
        },
        handlePaste(event, rowIndex, colIndex) {
            event.preventDefault()
            event.stopPropagation()
            const clipboardData = event.clipboardData
            const text = clipboardData.getData('text/plain');
            const pastedText = text.split('\n').map(line => line.split('\t').map(item => item.replace('\r', '')))
            // 如果最后一行没有数据，则删除
            if (pastedText[pastedText.length - 1].length === 1 && pastedText[pastedText.length - 1][0] === '') {
                pastedText.pop()
            }
            // 动态添加缺失的行
            const neededRows = rowIndex + pastedText.length;
            if (neededRows > this.dataSource.length) {
                const addCount = neededRows - this.dataSource.length;
                for (let i = 0; i < addCount; i++) {
                    const newRow = {
                        uuid: createUuid()
                    };
                    this.columns.forEach(col => {
                        newRow[col.key] = '';
                    });
                    this.dataSource.push(newRow);
                }
            }
            // 遍历粘贴的文本行和列
            pastedText.forEach((pastedRow, rowOffset) => {
                const targetRowIndex = rowIndex + rowOffset;
                if (targetRowIndex >= this.dataSource.length) return;
                pastedRow.forEach((cell, colOffset) => {
                    const targetColIndex = colIndex + colOffset;
                    if (targetColIndex >= this.columns.length) return;
                    this.dataSource[targetRowIndex][this.columns[targetColIndex].key] = cell;
                });
            });
        },
        handNameBlur(row, index) {
            onClickOther({element: this.element, clickName: 'onNameBlur', params: { newName: this.newName, row, index, activateText: this.activateText}})
            this.reName = ''
            if(isEmpty(this.newName)) return
            this.dataSource[index].name = this.newName
        },
        handleClickRow(e, row, index) {
            onClickOther({element: this.element, clickName:'onClickRow', params: { e, row, index, activateText: this.activateText } })
        },
        handleDbClickRow(e, row, index, col, colIndex) {
            this.reName = row.name
            this.newName = row.name
            onClickOther({element: this.element, clickName:'onDbClickRow', params: { e, row, index, col, colIndex, activateText: this.activateText} })
        },
        handleContextMenuRow(e, row, index) {
            onClickOther({element: this.element, clickName:'onContextMenuRow', params: { e, row, index, activateText: this.activateText} })
        },
        handleRowCheckbox(row, index, column) {
          onClickOther({element: this.element, clickName:'onClickCheckbox', params: { row, index, column, activateText: this.activateText }})
        },
        handleSelectChange(newVal, row, index, column) {
          onClickOther({element: this.element, clickName:'onClickSelectOption', params: { newVal, row, index, column, activateText: this.activateText }})
        },
        handleOperate(row, index, operate) {
            onClickOther({element: this.element, clickName:'onClickOperate', params: { row, index, operate, activateText: this.activateText }})
        },
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
        activateText: {
            get() {
                return getComputedGet('activateText', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('activateText', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
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
        visibleColumns () {
            return this.columns?.filter(col => col.visible !== false)
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
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    overflow-y: auto;
    user-select: text !important;
}
.nameText {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>