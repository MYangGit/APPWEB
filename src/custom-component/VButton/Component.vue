<template>
    <button :class="{disabledStyle: disabled}" class="v-button">{{ value }}</button>
</template>

<script>
import { getComputedGet, getComputedSet } from '../../utils/utils'
import { rootStore } from '@/stores/rootStore';

export default {
    props: {
        propValue: {
            type: Object,
            default: () => ({
                value: '',
                disabled: false
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    computed: {
        value: {
            get() {
                return getComputedGet('value', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('value', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
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
.disabledStyle {
    cursor: not-allowed;
    background-color: #f5f7fa;
    color: #c0c4cc;
    border-color: #ebeef5;
    pointer-events: none;
}
</style>
