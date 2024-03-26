<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="showBorder">
                    <el-checkbox v-model="curComponent.propValue.showBorder" label="显示边框" size="small" />
                </el-form-item>
                <el-form-item label="activeClickRow">
                    <el-checkbox v-model="curComponent.propValue.activeClickRow" label="可选中行" size="small" />
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
