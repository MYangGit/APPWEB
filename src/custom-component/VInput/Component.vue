<template>
    <div class="input-wrap">
        <label v-show="label">{{ label }}：</label>
        <el-input v-model="value" size="small" />
    </div>
</template>

<script>
import eventBus from '@/utils/eventBus';
import OnEvent from '../common/OnEvent'
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet } from '@/utils/utils';
export default {
    extends: OnEvent,
    props: {
        propValue: {
            type: Object,
            default: () => ({
                label: '',
                value: '',
            }),
        },
        element: {
            type: Object,
            default: () => {},
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
        }
    },
    watch: {
        propValue: {
            handler(val) {
                const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'updateValue');
                if (linkageEvents.length) {
                    eventBus.$emit('updateValue', linkageEvents, { ...val });
                }
            },
            deep: true,
            immediate: true,
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
