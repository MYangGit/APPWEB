<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="label">
                    <el-input v-model="curComponent.propValue.label" size="small" />
                </el-form-item>
                <el-form-item label="key">
                    <el-input v-model="curComponent.propValue.key" size="small" />
                </el-form-item>
                <el-form-item label="value">
                    <el-input v-model="curComponent.propValue.value" size="small" />
                </el-form-item>
                <el-form-item label="日期格式">
                    <el-select v-model="curComponent.propValue.valueFormat" size="small">
                        <el-option
                            v-for="item in valueOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                </el-form-item>
            </el-form>
        </CommonAttr>
    </div>
</template>

<script>
import CommonAttr from '@/custom-component/common/CommonAttr.vue'
import { rootStore } from '@/stores/rootStore';

export default {
    components: { CommonAttr },
    data() {
        return {
            valueOptions: [
                {
                    label: '年份',
                    value: 'year',
                },
                {
                    label: '月份',
                    value: 'month',
                },
                {
                    label: '周',
                    value: 'week',
                },
                {
                    label: '天',
                    value: 'date',
                },
            ],
        }
    },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
    },
}
</script>
