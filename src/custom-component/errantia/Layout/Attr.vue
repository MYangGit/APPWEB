<template>
    <div class="attr-list">
        <CommonAttr>
            <el-collapse v-model="activeNames">
                <el-collapse-item title="页眉" name="1">
                    <el-form>
                        <el-form-item label="isShow">
                            <el-checkbox v-model="curComponent.propValue.showHeader" size="small" />
                        </el-form-item>
                        <el-form-item label="height:">
                            <el-input 
                                v-model="curComponent.propValue.heightHeader" 
                                size="small" 
                                type="number"
                            />
                        </el-form-item>
                        <el-form-item label="背景色:">
                            <el-color-picker show-alpha v-model="curComponent.propValue.headerColor" />
                        </el-form-item>
                    </el-form>
                </el-collapse-item>
                <el-collapse-item title="左边栏" name="2">
                    <el-form>
                        <el-form-item label="isShow">
                            <el-checkbox v-model="curComponent.propValue.showLeftSidebar" size="small" />
                        </el-form-item>
                        <el-form-item label="width:">
                            <el-input 
                                 v-model="curComponent.propValue.widthLeftSidebar" 
                                 size="small" 
                                 type="number"
                            />
                        </el-form-item>
                        <el-form-item label="背景色:">
                            <el-color-picker show-alpha v-model="curComponent.propValue.leftSidebarColor" />
                        </el-form-item>
                    </el-form>
                </el-collapse-item>
                <el-collapse-item title="主界面" name="3">
                    <el-form>
                        <el-form-item label="背景色:">
                            <el-color-picker show-alpha v-model="curComponent.propValue.mainColor" />
                        </el-form-item>
                    </el-form>
                </el-collapse-item>
                <el-collapse-item title="右边栏" name="4">
                    <el-form>
                        <el-form-item label="isShow">
                            <el-checkbox v-model="curComponent.propValue.showRightSidebar"  size="small" />
                        </el-form-item>
                        <el-form-item label="width:">
                            <el-input 
                                v-model="curComponent.propValue.widthRightSidebar" 
                                size="small" 
                                type="number"
                            />
                        </el-form-item>
                        <el-form-item label="背景色:">
                            <el-color-picker show-alpha v-model="curComponent.propValue.rightSidebarColor" />
                        </el-form-item>
                    </el-form>
                </el-collapse-item>
                <el-collapse-item title="页脚" name="5">
                    <el-form>
                        <el-form-item label="isShow">
                            <el-checkbox v-model="curComponent.propValue.showFooter" size="small" />
                        </el-form-item>
                        <el-form-item label="height:">
                            <el-input 
                                v-model="curComponent.propValue.heightFooter" 
                                size="small" 
                                type="number"
                            />
                        </el-form-item>
                        <el-form-item label="背景色:">
                            <el-color-picker show-alpha v-model="curComponent.propValue.footerColor" />
                        </el-form-item>
                    </el-form>
                </el-collapse-item>
            </el-collapse>
        </CommonAttr>
    </div>
</template>

<script setup>
import { ref } from 'vue'
const activeNames = ref(['1'])
</script>

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
