<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="message">
                    <el-input v-model="curComponent.propValue.message" size="small" />
                </el-form-item>
                <el-form-item label="isLoading">
                    <el-checkbox v-model="curComponent.propValue.isLoading" label="加载中" size="small" />
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
