<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form-item label="domId">
                <el-input v-model="curComponent.propValue.domId" size="small" />
            </el-form-item>
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
