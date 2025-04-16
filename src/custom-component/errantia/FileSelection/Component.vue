<template>
    <div class="input-wrap">
        <label v-show="label">{{ label }}</label>
        <input
            type="file"
            :disabled="disabled"
            :style="{marginLeft: `${marginLeft}px`}"
            @change="handleFileChange"
        />
    </div>
</template>

<script>
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet } from '@/utils/utils';
import { useEventCentre } from '@/hooks/useEventCentre';

const { onChange } = useEventCentre();
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
        handleFileChange(newVal) {
          this.value = newVal.target.files[0];
          onChange({element: this.element, newValue: newVal})
        }
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
