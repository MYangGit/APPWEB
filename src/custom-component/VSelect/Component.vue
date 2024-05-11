<template>
    <div class="input-wrap">
        <label v-show="label">{{ label }}：</label>
        <el-select 
            v-model="value" 
            size="small" 
            placeholder="请选择"
            @change="handleValueChange"
        >
            <el-option
                v-for="item, index in options"
                :key="index"
                :label="item.label"
                :value="item.value"
            >
            </el-option>
        </el-select>
    </div>
</template>

<script>
import { getComputedGet, getComputedSet } from '../../utils/utils'
import { rootStore } from '@/stores/rootStore';
import { useEventCentre } from '@/hooks/useEventCentre';   

const { onChange } = useEventCentre();
export default {
    props: {
        propValue: {
            type: Object,
            default: () => ({
                value: '',
                options: [],
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
        label: {
            get() {
                return getComputedGet('label', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('label', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
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
        options: {
            get() {
                return getComputedGet('options', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('options', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
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
    -webkit-appearance: none;
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
