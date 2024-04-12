<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="禁止浮窗：">
                    <el-checkbox v-model="curComponent.propValue.disabled"  size="small" />
                </el-form-item>
                <el-form-item label="标题：">
                    <el-input  v-model="curComponent.propValue.title"  size="small" />
                </el-form-item>
                <el-form-item label="标题宽度：">
                    <el-input 
                        type="Number" 
                        v-model="curComponent.propValue.titleWidth" 
                        size="small" 
                    />
                </el-form-item>
                <el-form-item label="图标路径：">
                    <el-input  v-model="curComponent.propValue.iconPath"   size="small" />
                </el-form-item>
                <el-form-item label="水平排列：">
                    <el-checkbox v-model="curComponent.propValue.horizontal"  size="small" />
                </el-form-item>
                <el-form-item label="显示箭头：">
                    <el-checkbox v-model="curComponent.propValue.hasSubscript"  size="small" />
                </el-form-item>
                <span>触发方式：</span>
                <el-radio-group v-model="curComponent.propValue.trigger" class="ml-4">
                    <el-radio value="hover" size="large">悬浮</el-radio>
                    <el-radio value="click" size="large">点击</el-radio>
                    <el-radio value="contextmenu" size="large">右键</el-radio>
                </el-radio-group>
                <el-form-item label="width:">
                    <el-input 
                        type="Number" 
                        v-model="curComponent.propValue.floatWidth" 
                        size="small" 
                    />
                </el-form-item>
                <el-form-item label="height:">
                    <el-input 
                        type="Number" 
                        v-model="curComponent.propValue.floatHeight" 
                        size="small" 
                    />
                </el-form-item>
                <el-form-item label="marginLeft:">
                    <el-input 
                        type="Number" 
                        v-model="curComponent.propValue.marginLeft" 
                        size="small" 
                    />
                </el-form-item>
            </el-form>
        </CommonAttr>
    </div>
</template>

<script>
import generateID from '@/utils/generateID';
import CommonAttr from '@/custom-component/common/CommonAttr.vue';
import { rootStore } from '@/stores/rootStore';
export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
        options() {
            return rootStore.dataCenter.curComponent.propValue.panelLists
        },
    },
    methods: {
       
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
.header-icon {
    margin-right: 20px;
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
