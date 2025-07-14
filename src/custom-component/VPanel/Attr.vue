<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="背景图片地址：">
                        <el-input 
                            v-model="curComponent.propValue.srcPath" 
                            size="small" 
                            type="textarea" 
                        />
                </el-form-item>
                <el-form-item label="是否裁剪覆盖：">
                    <el-switch 
                        v-model="curComponent.propValue.cutAndCover" 
                        size="small" 
                    />
                </el-form-item>
            </el-form>
        </CommonAttr>
    </div>
</template>

<script>
import CommonAttr from '@/custom-component/common/CommonAttr.vue';
import { rootStore } from '@/stores/rootStore';

export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
    },
};
</script>

<style lang="less" scoped>
.tab-item {
    margin: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    .el-input {
        display: inline-block;
        width: 90%;
    }
    .el-icon-close {
        cursor: pointer;
    }
}
.attr-title {
    color: #303133;
    font-size: 14px;
    margin: 10px 0 5px;
}
.attr-btn {
    padding: 0 5px;
    .el-button {
        width: 90%;
    }
}
</style>
