<template>
    <div class="input-wrap">
        <el-tree
            style="width: 100%; height: 100%;"
            :data="options"
            show-checkbox
            node-key="id"
            :props="defaultProps"
        />
    </div>
</template>

<script>
import { getComputedGet, getComputedSet } from '@/utils/utils';
import { rootStore } from '@/stores/rootStore';
import { useEventCentre } from '@/hooks/useEventCentre';   

const { onChange } = useEventCentre();
export default {
    data() {
        return {
            defaultProps: {
                children: 'children',
                label: 'label',
            },
        }
    },
    props: {
        propValue: {
            type: Object,
            default: () => ({
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
        handleValueChange(newVal) {
            onChange({element: this.element, newValue: newVal})
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
                return getComputedGet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
    }
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
