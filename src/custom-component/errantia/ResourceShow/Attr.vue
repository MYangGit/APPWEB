<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="src地址">
                    <el-input 
                        v-model="curComponent.propValue.srcPath" 
                        size="small" 
                        type="textarea" 
                    />
                </el-form-item>
                <el-form-item label="Base64格式">
                    <el-checkbox 
                        v-model="curComponent.propValue.base64" 
                        label="Base64" 
                        size="small" 
                    />
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
