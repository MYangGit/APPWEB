<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="手风琴：">
                    <el-checkbox v-model="curComponent.propValue.accordion"  size="small" />
                </el-form-item>
                <el-form-item label="箭头紧靠：">
                    <el-checkbox v-model="curComponent.propValue.arrowNear"  size="small" />
                </el-form-item>
                <el-form-item label="箭头方向：">
                    <el-radio-group v-model="curComponent.propValue.arrowPosition" class="ml-4">
                        <el-radio value="left" size="large">left</el-radio>
                        <el-radio value="right" size="large">right</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="折叠面板：">
                    <el-button size="small" @click="handAddCollapse">+</el-button>
                </el-form-item>
            </el-form>
            <el-collapse>
                <el-collapse-item 
                    v-for="item,index in options" 
                    :key="item.name"
                    :name="item.name"
                >
                    <template #title>
                        <el-icon 
                            v-if="item.name !== '1'"
                            class="header-icon" 
                            @click.stop="handDelete(index)"
                        >
                            <CircleClose />
                        </el-icon>
                        面板{{item.name}}
                    </template>
                    <el-form>
                        <br/>
                        <el-form-item label="title:">
                            <el-input v-model="item.title" size="small" />
                        </el-form-item>
                        <el-form-item label="height:">
                            <el-input 
                                type="Number" 
                                v-model="item.height" 
                                size="small" 
                            />
                        </el-form-item>
                    </el-form>
                </el-collapse-item>
            </el-collapse>
        </CommonAttr>
    </div>
</template>

<script>
import generateID from '@/utils/generateID';
import CommonAttr from '@/custom-component/common/CommonAttr.vue';
import { rootStore } from '@/stores/rootStore';
let count = 1
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
        handDelete(index) {
            this.options.splice(
                index,
                1,
            )
            // 第一项是剩余空间，所以整体加一同步item与options
            this.curComponent.items.splice(index + 1, 1)
        },
        handAddCollapse() {
            count++
            const length = this.curComponent.items.length
            this.options.push({
                title: "面板" + count,
                name: count,
                height: 100,
            })
            this.curComponent.items.push({
                name: generateID(),
                label: `ErCollapse${count}`,
            })
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
