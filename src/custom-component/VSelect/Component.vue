<template>
    <div class="input-wrap">
        <label v-show="label">{{ label }}：</label>
        <el-select 
            v-model="value" 
            size="small" 
            placeholder="请选择"
            @change="handleValueChange"
            :disabled="disabled"
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
import { getComputedGet, getComputedSet, isEmpty } from '../../utils/utils'
import { rootStore } from '@/stores/rootStore';
import { useEventCentre } from '@/hooks/useEventCentre';   

const { onChange } = useEventCentre();
export default {
    props: {
        propValue: {
            type: Object,
            default: () => ({
                value: '',
                disabled: false,
                options: [],
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    methods: {
        isEmpty,
        handleValueChange(newVal) {
            let params = {}
            if(this.options.length > 0){
                const findItem = this.options.find(item => item.value === newVal)
                if(findItem){
                    params = findItem
                }
            }
            onChange({element: this.element, newValue: newVal, params})
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
        disabled: {
            get() {
                const disVal = getComputedGet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
                // 判断是否为布尔
                if(typeof disVal === "boolean"){
                    return disVal
                }
                return this.isEmpty(disVal)
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
