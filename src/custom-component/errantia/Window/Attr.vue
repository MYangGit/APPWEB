<template>
    <div>
        <CommonAttr>
            <el-form>
                <el-form-item label="匹配内容选中：">
                    <el-input  v-model="curComponent.propValue.funParam"  size="small" />
                </el-form-item>
                <el-form-item label="新增窗口：">
                    <el-button size="small" @click="handleAdd()">+</el-button>
                </el-form-item>
                <el-collapse>
                    <el-collapse-item 
                        v-for="item,index in winDataoOptions" 
                        :key="item.uuid"
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
                            <el-form-item label="内容类型:">
                                <el-input 
                                    type="text" 
                                    v-model="item.contentType" 
                                    size="small" 
                                />
                            </el-form-item>
                            <el-form-item label="left:">
                                <el-input 
                                    type="text" 
                                    v-model="item.style.left" 
                                    size="small" 
                                />
                            </el-form-item>
                            <el-form-item label="top:">
                                <el-input 
                                    type="text" 
                                    v-model="item.style.top" 
                                    size="small" 
                                />
                            </el-form-item>
                            <el-form-item label="width:">
                                <el-input 
                                    type="Number" 
                                    v-model="item.style.width" 
                                    size="small" 
                                />
                            </el-form-item>
                            <el-form-item label="height:">
                                <el-input 
                                    v-model="item.style.height" 
                                    size="small" 
                                />
                            </el-form-item>
                            <el-form-item label="dataSource:">
                                <el-input 
                                    type="textarea"
                                    v-model="item.propValue.dataSource" 
                                    size="small" 
                                />
                            </el-form-item>
                            <el-form-item label="layout:">
                                <el-input 
                                    type="textarea"
                                    v-model="item.propValue.layout" 
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
import { getComputedGet, getComputedSet, createUuid, nameRepeat } from '@/utils/utils'

export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
        winDataoOptions:{
            get() {
                return getComputedGet('winDataList', this.curComponent.dataBinds, rootStore.dataConfig.stateSet, this.curComponent.propValue)
            },
            set(val) {
                getComputedSet('winDataList', this.curComponent.dataBinds, rootStore.dataConfig.stateSet, this.curComponent.propValue, val)
            }
        },
    },
    methods: {
        handleAdd() {
            let title = `新窗口${this.winDataoOptions.length + 1}`
            title = nameRepeat(title, this.winDataoOptions, '')
            const newItem = {
                uuid: createUuid(),
                title: title,
                isMaximized: false,
                isMinimized: false,
                contentType: 'plot',
                style: {
                    width: 150,
                    height: 150,
                    left: 0,
                    top: 0,
                    rotate: 0,
                    pointerEvents: "all",
                },
                lastStyle: {},
                propValue: {},
            };
            this.winDataoOptions.push(newItem);    
        },
        handDelete(index) {
            this.winDataoOptions.splice(index, 1);
        },
    },
};
</script>

<style lang="less" scoped>
</style>
