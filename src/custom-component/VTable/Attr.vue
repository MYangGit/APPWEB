<template>
    <div class="attr-list v-talbe-attr">
        <CommonAttr>
            <EditTable></EditTable>
            <el-form>
                <el-form-item label="斑马纹">
                    <el-switch v-model="propValue.stripe"></el-switch>
                </el-form-item>
                <el-form-item label="边框">
                    <el-switch v-model="propValue.border"></el-switch>
                </el-form-item>
            </el-form>
        </CommonAttr>
    </div>
</template>

<script>
import CommonAttr from '@/custom-component/common/CommonAttr'
import EditTable from './EditTable'

export default {
    components: { EditTable, CommonAttr },
    computed: {
        propValue() {
            return rootStore.dataCenter.curComponent.propValue
        },
    },
}
</script>
