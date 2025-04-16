<template>
    <div class="input-wrap">
        <label v-show="label">{{ label }}：</label>
        <el-checkbox-group  
          v-model="value"
          :disabled="disabled"
          @change="handleValueChange"
        >
            <el-checkbox 
                v-for="item, index in options"
                :key="index"
                :label="item.label"
                :value="item.value"
            ></el-checkbox>
        </el-checkbox-group>
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
                disabledText: "",
                label: '',
                disabled: false,
                value: [],
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
        disabled: {
            get() {
                let disVal =  getComputedGet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
                if(typeof disVal === "boolean"){
                    if(this.propValue.disabledText === "!"){
                       return !disVal
                    }
                    return disVal
                }
                if(!this.isEmpty(this.propValue.disabledText)){
                    return (disVal === this.propValue.disabledText)
                }
                return this.isEmpty(disVal)
            },
            set(val) {
                getComputedSet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
    },
}
</script>

<style lang="less" scoped>
.el-checkbox-group {
    display: inline-block;
}
</style>
