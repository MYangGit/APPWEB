<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <span>对齐方式：</span>
                <el-radio-group v-model="curComponent.propValue.textAlign" class="ml-4">
                    <el-radio value="left" size="large">靠左</el-radio>
                    <el-radio value="center" size="large">居中</el-radio>
                    <el-radio value="right" size="large">靠右</el-radio>
                </el-radio-group>
                <el-form-item label="显示边框：">
                    <el-checkbox v-model="curComponent.propValue.showBorder" size="small" />
                </el-form-item>
                <el-form-item label="可选中行：">
                    <el-checkbox v-model="curComponent.propValue.activeClickRow" size="small" />
                </el-form-item>
                <el-form-item label="选中uuid：">
                    <el-input v-model="curComponent.propValue.currUuid" size="small" />
                </el-form-item>
                <el-form-item label="操作：">
                    <el-checkbox 
                        v-model="curComponent.propValue.showOperate" 
                        size="small"
                        @change="handleShowOperate"
                    />
                </el-form-item>
                <el-form-item label="编号：">
                    <el-checkbox 
                        v-model="curComponent.propValue.serialNumber" 
                        size="small"
                        @change="handleSerialNumber"
                    />
                </el-form-item>
                <el-form-item label="新增列菜单：">
                    <el-button size="small" @click="handleAdd()">+</el-button>
                </el-form-item>
                <el-collapse>
                    <el-collapse-item 
                        v-for="item,index in options" 
                        :key="item.key"
                        :name="item.title"
                    >
                        <template #title>
                            <el-icon 
                                class="header-icon" 
                                @click.stop="handDelete(index)"
                            >
                                <CircleClose />
                            </el-icon>
                            {{item.title}}
                        </template>
                        <el-form>
                            <br/>
                            <el-form-item label="标题:">
                                <el-input 
                                    type="text" 
                                    v-model="item.title" 
                                    size="small" 
                                />
                            </el-form-item>
                            <el-form-item label="key:">
                                <el-input 
                                    type="text" 
                                    v-model="item.key" 
                                    size="small" 
                                />
                            </el-form-item>
                            <el-form-item label="width:">
                                <el-input 
                                    type="Number" 
                                    v-model="item.width" 
                                    size="small" 
                                />
                            </el-form-item>
                            <el-form-item label="slot:">
                                <el-input 
                                    v-model="item.slot" 
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
import CommonAttr from '@/custom-component/common/CommonAttr.vue'
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet } from '@/utils/utils'

export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
        options:{
            get() {
                return getComputedGet('columns', this.curComponent.dataBinds, rootStore.dataConfig.stateSet, this.curComponent.propValue)
            },
            set(val) {
                getComputedSet('columns', this.curComponent.dataBinds, rootStore.dataConfig.stateSet, this.curComponent.propValue, val)
            }
        },
    },
    methods: {
        handleShowOperate(val) {
            if (val) {
                this.curComponent.propValue.columns.push({
                    title: '操作',
                    key: 'operate',
                    slot: 'operate'
                })
            } else {
                this.curComponent.propValue.columns = this.curComponent.propValue.columns.filter(item => item.key !== 'operate')
            }
        },
        handleSerialNumber(val) {
            if (val) {
                this.curComponent.propValue.columns.unshift({
                    title: '编号',
                    key: 'serialNumber',
                    slot: 'serialNumber'
                })
            } else {
                this.curComponent.propValue.columns = this.curComponent.propValue.columns.filter(item => item.key !== 'serialNumber')
            }
        },
        handleAdd() {
            this.options.push({
                title: '列' + (this.options.length + 1),
                key: 'column' + (this.options.length + 1),
            })
        },
        handDelete(index) {
            this.options.splice(index, 1)
        }
    }
}
</script>

<style lang="less" scoped>
.header-icon {
    cursor: pointer;
    margin-right: 10px;
}
</style>
