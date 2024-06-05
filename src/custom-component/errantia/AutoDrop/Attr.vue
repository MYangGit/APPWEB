<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="禁用：">
                    <el-checkbox v-model="curComponent.propValue.disabled"  size="small" />
                </el-form-item>
                <el-form-item label="选中：">
                    <el-checkbox v-model="curComponent.propValue.activate"  size="small" />
                </el-form-item>
                <el-form-item label="匹配内容选中：">
                    <el-input  v-model="curComponent.propValue.activateText"  size="small" />
                </el-form-item>
                <span>触发方式：</span>
                <el-radio-group v-model="curComponent.propValue.trigger" class="ml-4">
                    <el-radio value="hover" size="large">悬浮</el-radio>
                    <el-radio value="click" size="large">点击</el-radio>
                    <el-radio value="contextmenu" size="large">右键</el-radio>
                </el-radio-group>
                <el-form-item label="浮窗宽度:">
                    <el-input 
                        type="Number" 
                        v-model="curComponent.propValue.floatWidth" 
                        size="small" 
                    />
                </el-form-item>
                <el-form-item label="浮窗高度:">
                    <el-input 
                        type="Number" 
                        v-model="curComponent.propValue.floatHeight" 
                        size="small" 
                    />
                </el-form-item>
                <el-form-item label="新增悬浮菜单：">
                    <el-button size="small" @click="handleAdd()">+</el-button>
                </el-form-item>
                <el-collapse>
                    <el-collapse-item 
                        v-for="item,index in options" 
                        :key="item.command"
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
                            <el-form-item label="分割线:">
                                <el-checkbox v-model="item.divided"  size="small" />
                            </el-form-item>
                            <el-form-item label="点击命令(不能重复)：">
                                <el-input 
                                    type="text" 
                                    v-model="item.command" 
                                    size="small" 
                                />
                            </el-form-item>
                            <el-form-item label="名称:">
                                <el-input 
                                    type="text" 
                                    v-model="item.name" 
                                    size="small" 
                                />
                            </el-form-item>
                        </el-form>
                    </el-collapse-item>
                </el-collapse>
            </el-form>
        </CommonAttr>
    </div>
</template>

<script>
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
                return getComputedGet('dropdownMenu', this.curComponent.dataBinds, rootStore.dataConfig.stateSet, this.curComponent.propValue)
            },
            set(val) {
                getComputedSet('dropdownMenu', this.curComponent.dataBinds, rootStore.dataConfig.stateSet, this.curComponent.propValue, val)
            }
        },
    },
    methods: {
        handleAdd() {
            let name = 'Action ' + (this.options.length + 1)
            name = nameRepeat(name, this.options, '')
            const item = {
                name,
                command: name,
                disabled: false,
                divided: false,
            }
            this.options.push(item)
        },
        handDelete(index) {
            this.options.splice(index, 1)
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
