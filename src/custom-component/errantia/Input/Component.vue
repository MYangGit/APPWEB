<template>
    <div class="input-wrap">
        <label v-show="label">{{ label }}</label>
        <el-input 
            :style="{marginLeft: `${marginLeft}px`}"
            v-model.lazy="value" 
            size="small"
            :disabled="disabled"
            @focus="handleFocus"
            @change="handleValueChange"
            @blur="handleValublur"
        />
    </div>
</template>

<script>
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet } from '@/utils/utils';
import { useEventCentre } from '@/hooks/useEventCentre';

const { onChange, onClickOther } = useEventCentre();
export default {
    props: {
        propValue: {
            type: Object,
            default: () => ({
                label: '',
                value: '',
                disabled: false,
                marginLeft: 6,
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    methods: {
        handleFocus() {
            this.oldValue = this.value
        },
        handleValublur() {
           onClickOther({element: this.element, clickName: 'blur', params: { newVal: this.value }})
        },
        handleValueChange(newVal) {
          onChange({element: this.element, newValue: newVal, oldValue: this.oldValue})
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
        disabled: {
            get() {
                return getComputedGet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        marginLeft: {
            get() {
                return getComputedGet('marginLeft', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('marginLeft', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
    },
}
</script>

<style lang="less" scoped>
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
