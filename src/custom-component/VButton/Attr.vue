<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="内容">
                    <el-input v-model="curComponent.propValue.value" type="textarea" :rows="3" />
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
