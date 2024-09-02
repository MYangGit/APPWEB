<template>
    <div class="attr-list">
        <CommonAttr>
            <div class="attr-title">选项卡</div>
            <el-form-item label="选中tab名">
                <el-input v-model="curComponent.propValue.autoActiveName" size="small" />
            </el-form-item>
            <el-form-item label="禁用tab名">
                <el-input v-model="curComponent.propValue.visibleName" size="small" />
            </el-form-item>
            <div v-for="(tab, index) in curComponent.tabs" :key="tab.name" class="tab-item">
                <el-input v-model="tab.label" />
                <i class="el-icon-close" @click="handleDelete(index)"></i>
            </div>
            <div class="attr-btn">
                <el-button @click="handleAdd()">新增选项卡</el-button>
            </div>
            <div class="attr-title">位置</div>
            <el-radio-group v-model="curComponent.position" style="margin-bottom: 30px">
                <el-radio-button value="top">top</el-radio-button>
                <el-radio-button value="right">right</el-radio-button>
                <el-radio-button value="bottom">bottom</el-radio-button>
                <el-radio-button value="left">left</el-radio-button>
            </el-radio-group>
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
    },
    methods: {
        handleDelete(index) {
            this.curComponent.tabs.splice(index, 1);
        },
        handleAdd() {
            this.curComponent.tabs.push({
                name: generateID(),
                label: `Tab${this.curComponent.tabs.length + 1}`,
            });
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
