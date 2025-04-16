<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="禁用">
                    <el-checkbox v-model="curComponent.propValue.disabled" size="small" />
                </el-form-item>
                <el-form-item label="图标">
                    <el-input v-model="curComponent.propValue.className" size="small" />
                </el-form-item>
                <el-form-item label="图标库">
                    <a href="https://element-plus.org/zh-CN/component/icon.html" target="_blank">更多图标</a>
                </el-form-item>
                <el-form-item label="自定义点击参数">
                    <el-input v-model="curComponent.propValue.activateText" size="small" />
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
