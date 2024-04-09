<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="方向">
                    <el-select v-model="curComponent.propValue.direction">
                        <el-option
                            v-for="item in ['row', 'column']"
                            :key="item"
                            :label="item"
                            :value="item"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="水平对齐">
                    <el-select v-model="curComponent.propValue.horAlign">
                        <el-option
                            v-for="item in ['start', 'center', 'end', 'space-between', 'space-around']"
                            :key="item"
                            :label="item"
                            :value="item"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="垂直对齐">
                    <el-select v-model="curComponent.propValue.verAlign">
                        <el-option
                            v-for="item in ['start', 'center', 'end']"
                            :key="item"
                            :label="item"
                            :value="item"
                        />
                    </el-select>
                </el-form-item>
                <el-form-item label="是否换行">
                    <el-select v-model="curComponent.propValue.wrapType">
                        <el-option
                            v-for="item in ['wrap', 'nowrap']"
                            :key="item"
                            :label="item"
                            :value="item"
                        />
                    </el-select>
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
