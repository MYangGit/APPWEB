<template>
    <div class="input-wrap">
        <el-tree
            ref="treeRef"
            style="width: 100%; height: 100%;"
            :style="{ backgroundColor: element.style?.backgroundColor || 'transparent', color: `${element.style?.color} !important` || '#000' }"
            show-checkbox
            check-on-click-node
            :expand-on-click-node = "false"
            :default-expand-all="propValue.defaultExpandAll"
            :data="options"
            :node-key="propValue.nodeKey"
            :props="defaultProps"
            @check-change="handleValueChange"
        />
    </div>
</template>

<script>
import { getComputedGet, getComputedSet } from '@/utils/utils';
import { rootStore } from '@/stores/rootStore';
import { useEventCentre } from '@/hooks/useEventCentre'; 

const { onClickOther } = useEventCentre();
export default {
    data() {
        return {
            defaultProps: {
                children: 'children',
                label: 'label',
                disable: 'disabled',
            },
        }
    },
    props: {
        propValue: {
            type: Object,
            default: () => ({
                nodeKey: "id",
                defaultExpandAll: false,
                value:[],
                activateText: "",
                disabled: false,
                options: [
                    {
                        id: 1,
                        label: '一级 1',
                        children: [
                            {
                                id: 4,
                                label: '二级 1-1',
                                children: [
                                    {
                                        id: 9,
                                        label: '三级 1-1-1'
                                    },
                                    {
                                        id: 10,
                                        label: '三级 1-1-2'
                                    }
                                ]
                            }
                        ],
                    },
                    {
                        id: 2,
                        label: '一级 2',
                        children: [
                            {
                                id: 5,
                                label: '二级 2-1'
                            },
                            {
                                id: 6,
                                label: '二级 2-2'
                            }
                        ],
                    }, 
                ],
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    methods: {
        handleValueChange(data, checked, indeterminate) {
            onClickOther({element: this.element, clickName: 'clickTree', params: { data, checked, indeterminate, activateText:this.activateText, treeRef: this.$refs.treeRef}})
        },
    },
    computed: {
        options: {
            get() {
                return getComputedGet('options', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('options', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        disabled: {
            get() {
                let disVal =  getComputedGet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
                return disVal
            },
            set(val) {
                getComputedSet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        activateText: {
            get() {
                return getComputedGet('activateText', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('activateText', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        value: {
            get() {
                return getComputedGet('value', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('value', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
    },
    mounted() {
        onClickOther({element: this.element, clickName: 'mounted', params: { activateText:this.activateText,  treeRef: this.$refs.treeRef }})
    },
}
</script>

<style lang="less" scoped>
.v-button {
    display: inline-block;
    line-height: 1;
    white-space: nowrap;
    cursor: pointer;
    background: #fff;
    border: 1px solid #dcdfe6;
    color: #606266;
    text-align: center;
    box-sizing: border-box;
    outline: 0;
    margin: 0;
    transition: .1s;
    font-weight: 500;
    width: 100%;
    height: 100%;
    font-size: 14px;

    &:active {
        color: #3a8ee6;
        border-color: #3a8ee6;
        outline: 0;
    }

    &:hover {
        background-color: #ecf5ff;
        color: #3a8ee6;
    }
}
.input-wrap {
    display: inline-flex;
    align-items: center;
    label {
        word-break: keep-all;
        white-space: nowrap;
        margin-bottom: 0;
    }
}
</style>

<style>
.el-text {
    color: #fff !important;
}
</style>
