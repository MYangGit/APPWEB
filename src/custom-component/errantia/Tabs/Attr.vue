<template>
    <div class="attr-list">
        <CommonAttr>
            <div class="attr-title">位置</div>
            <el-radio-group v-model="curComponent.position" style="margin-bottom: 30px">
                <el-radio-button value="top">top</el-radio-button>
                <el-radio-button value="right">right</el-radio-button>
                <el-radio-button value="bottom">bottom</el-radio-button>
                <el-radio-button value="left">left</el-radio-button>
            </el-radio-group>
            <el-form-item label="新增选项卡：">
                <el-button size="small" @click="handleAdd()">+</el-button>
            </el-form-item>
            <el-collapse>
                <el-collapse-item 
                    v-for="item,index in options" 
                    :key="item.name"
                    :name="item.name"
                >
                    <template #title>
                        <el-icon 
                            class="header-icon" 
                            @click.stop="handDelete(index)"
                        >
                            <CircleClose />
                        </el-icon>
                        {{item.name}}
                    </template>
                    <el-form>
                        <br/>
                        <el-form-item label="禁用:">
                            <el-checkbox v-model="item.disabled"  size="small" />
                        </el-form-item>
                        <el-form-item label="可删除:">
                            <el-checkbox v-model="item.closable"  size="small" />
                        </el-form-item>
                        <el-form-item label="显示：">
                            <el-checkbox v-model="item.visible"  size="small" />
                        </el-form-item>
                        <el-form-item label="标题:">
                            <el-input 
                                type="text" 
                                v-model="item.label" 
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
import { getComputedGet, getComputedSet, nameRepeat } from '@/utils/utils';

export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
        options:{
            get() {
                return getComputedGet('tabsItem', this.curComponent.dataBinds, rootStore.dataConfig.stateSet, this.curComponent.propValue)
            },
            set(val) {
                getComputedSet('tabsItem', this.curComponent.dataBinds, rootStore.dataConfig.stateSet, this.curComponent.propValue, val)
            }
        },
    },
    methods: {
        handDelete(index) {
            this.options.splice(
                index,
                1,
            )
            this.curComponent.items.splice(index, 1)
        },
        handleAdd() {
            let name = `ErTabs${this.options.length + 1}`
            name = nameRepeat(name, this.options, '')
            this.options.push({
                name,
                label: name,
                closable: false,
                disabled: false,
                visible: true,
            })
            this.curComponent.items.push({
                name: generateID(),
                label: name,
            })
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
.header-icon {
    cursor: pointer;
    margin-right: 10px;
}
</style>
