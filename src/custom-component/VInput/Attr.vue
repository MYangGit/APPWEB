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
            </el-form>
        </CommonAttr>
    </div>
</template>

<script>
import CommonAttr from '@/custom-component/common/CommonAttr.vue'
import { rootStore } from '@/stores/rootStore';

export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
    },
}
</script>
