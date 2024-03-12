<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="列数">
                    <el-input-number v-model="curComponent.cols" :min="1" @change="handleChange" />
                </el-form-item>
                <el-form-item label="行数">
                    <el-input-number v-model="curComponent.rows" :min="1" @change="handleChange" />
                </el-form-item>
            </el-form>
        </CommonAttr>
    </div>
</template>

<script>
import generateID from '@/utils/generateID'
import CommonAttr from '@/custom-component/common/CommonAttr.vue'
import { rootStore } from '@/stores/rootStore';

export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
    },
    methods: {
        handleChange() {
            const count = this.curComponent.cols * this.curComponent.rows
            const length = this.curComponent.items.length
            if (count > length) {
                new Array(count - length).fill(1).forEach(() => {
                    this.curComponent.items.push({
                        name: generateID(),
                        label: 'Grid',
                    })
                })
            } else if (count < length) {
                this.curComponent.items.splice(count, length - count)
            }
        },
    },
}
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
