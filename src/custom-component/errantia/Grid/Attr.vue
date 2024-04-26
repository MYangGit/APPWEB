<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="列数">
                    <el-input-number 
                        v-model="curComponent.propValue.cols" 
                        :min="1" 
                     />
                </el-form-item>
                <el-form-item label="行数">
                    <el-input-number 
                        v-model="curComponent.propValue.rows" 
                        :min="1" 
                    />
                </el-form-item>
                <el-form-item label="列间距">
                    <el-input
                        type="Number"
                        v-model="curComponent.propValue.cgap"
                    />
                </el-form-item>
                <el-form-item label="行间距">
                    <el-input
                        type="Number"
                        v-model="curComponent.propValue.rgap"
                    />
                </el-form-item>
                <el-form-item label="先行后列：">
                    <el-checkbox v-model="curComponent.propValue.autoFlowRow"  size="small" />
                </el-form-item>
                <el-form-item label="添加容器：">
                    <el-button size="small" @click="handAddGrid">+</el-button>
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
                            class="header-icon" 
                            @click.stop="handDelete(index)"
                        >
                            <CircleClose />
                        </el-icon>
                        {{item.name}}
                    </template>
                    <el-form>
                        <br/>
                        <el-form-item label="显示：">
                            <el-checkbox v-model="item.visible"  size="small" />
                        </el-form-item>
                        <el-form-item label="跨越列:">
                            <el-input 
                                type="Number"
                                :min="1"   
                                v-model="item.cSpan" 
                                size="small" 
                            />
                        </el-form-item>
                        <el-form-item label="跨越行:">
                            <el-input 
                                type="Number"
                                :min="1"  
                                v-model="item.rSpan" 
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
import CommonAttr from '@/custom-component/common/CommonAttr.vue';
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet } from '@/utils/utils';
import generateID from '@/utils/generateID';
import { nameRepeat } from '@/utils/utils';

export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
        options:{
            get() {
                return getComputedGet('gridItems', this.curComponent.dataBinds, rootStore.dataConfig.stateSet, this.curComponent.propValue)
            },
            set(val) {
                getComputedSet('gridItems', this.curComponent.dataBinds, rootStore.dataConfig.stateSet, this.curComponent.propValue, val)
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
        handAddGrid() {
            let name = `ErGrid${this.options.length + 1}`
            name = nameRepeat(name, this.options, '')
            this.options.push({
                name,
                visible: true,
                cSpan: 1,
                rSpan: 1,
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
.header-icon {
    margin-right: 20px;
}
.attr-btn {
    padding: 0 5px;
    .el-button {
        width: 90%;
    }
}
</style>
