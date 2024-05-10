<template>
    <div class="input-wrap">
        <label v-show="label">{{ label }}：</label>
        <el-checkbox-group  
          v-model="value"
          @change="handleValueChange"
        >
            <el-checkbox 
                v-for="item, index in options"
                :key="index"
                :value="item.value"
                :label="item.label"
            ></el-checkbox>
        </el-checkbox-group>
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
                label: '',
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
    },
}
</script>

<style lang="less" scoped>
.el-checkbox-group {
    display: inline-block;
}
</style>
