<template>
    <div class="input-wrap">
        <el-table size="small" :data="tableData">
            <el-table-column type="index" label="编号" width="50" />
            <el-table-column prop="dataType" label="数据类型" width="120">
                <template #default="scope">
                    <el-select
                        v-model="scope.row.dataType"
                        placeholder="数据类型"
                        size="small"
                        style="width: 100px"
                        >
                        <el-option
                            v-for="item in dataTypeOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column prop="algorithm" label="算法" width="90">
                <template #default="scope">
                    <el-select
                        v-model="scope.row.algorithm"
                        placeholder="算法"
                        size="small"
                        style="width: 80px"
                        >
                        <el-option
                            v-for="item in algorithmOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column prop="filePath" label="文件选择" width="120">
                <template #default="scope">
                    <el-select
                        multiple
                        :multiple-limit="2"
                        v-model="scope.row.filePath"
                        placeholder=""
                        size="small"
                        style="width: 100px"
                        >
                        <el-option
                            v-for="item in filesList"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column prop="figureColor" label="颜色" width="50">
                <template #default="scope">
                    <el-color-picker size="small" v-model="scope.row.figureColor" />
                </template>
            </el-table-column>
            <el-table-column prop="legend" label="图例" width="100">
                <template #default="scope">
                    <el-input size="small" type="text" v-model="scope.row.legend" />
                </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
                <template #header>
                    操作 <el-button size="small" :icon="Plus" circle @click="handleAdd"/>
                </template>
                <template #default="scope">
                    <el-button size="small" :icon="Delete" circle  @click="handleDelete(scope.$index)"/>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { getComputedGet, getComputedSet } from '../../utils/utils'
import { rootStore } from '@/stores/rootStore';
import {
  Plus,
  Delete
} from '@element-plus/icons-vue'

const dataTypeOptions = ref([
    {
        label: "Float64",
        value: "Float64"
    }
])

const algorithmOptions = ref([
    {
        label: "PSD",
        value: "PSD"
    },
    {
        label: "ABS",
        value: "ABS"
    },
    {
        label: "请选择",
        value: ""
    }
])

const props = defineProps({
    propValue: {
        type: Object,
        default: () => ({
            value: [],
            fileList: [],
        })
    },
    element: {
        type: Object,
        default: () => {},
    },
})

const filesList = computed(() => {
    return getComputedGet('fileList', props.element.dataBinds, rootStore.dataConfig.stateSet, props.propValue)
})

const tableData = computed(() => {
    return getComputedGet('value', props.element.dataBinds, rootStore.dataConfig.stateSet, props.propValue)
})


const handleAdd = () => { 
    tableData.value.push({
        dataType: 'Int',
        algorithm: 'ABS',
        filePath: [],
        figureColor: "#409EFF",
        legend: "chart"
    })
    getComputedSet('value', props.element.dataBinds, rootStore.dataConfig.stateSet, props.propValue, tableData.value)
}

const handleDelete = (index) => {
    tableData.value.splice(index, 1)
    getComputedSet('value', props.element.dataBinds, rootStore.dataConfig.stateSet, props.propValue, tableData.value)
}
</script>

<style lang="less" scoped>
.input-wrap {
    display: inline-flex;
    align-items: baseline;
}
</style>
