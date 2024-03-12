<template>
    <div class="attr-list">
        <CommonAttr>
            <div class="attr-title">是否展示checkBox</div>
            <el-radio-group v-model="propValue.isShowCheck" style="margin-bottom: 30px">
                <el-radio :value="true">是</el-radio>
                <el-radio :value="false">否</el-radio>
            </el-radio-group>
            <div class="attr-title">是否懒加载</div>
            <el-radio-group v-model="propValue.isLazy" style="margin-bottom: 30px">
                <el-radio :value="true">是</el-radio>
                <el-radio :value="false">否</el-radio>
            </el-radio-group>
            <div class="attr-title">props</div>
            <el-form>
                <el-form-item label="children">
                    <el-input v-model="propValue.props.children" />
                </el-form-item>
                <el-form-item label="label">
                    <el-input v-model="propValue.props.label" />
                </el-form-item>
                <el-form-item label="isLeaf">
                    <el-input v-model="propValue.props.isLeaf" />
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
        propValue() {
            return rootStore.dataCenter.curComponent.propValue;
        },
    },
};
</script>
<style lang="less" scoped>
.attr-title {
    color: #303133;
    font-size: 14px;
    margin: 10px 0 5px;
}
</style>
