<template>
    <div class="input-wrap">
        <el-input class="input-textarea" v-model="value" size="small" type="textarea" />
    </div>
</template>

<script>
import eventBus from '@/utils/eventBus';
import OnEvent from '../common/OnEvent'
import { getComputedGet, getComputedSet } from '../../utils/utils'
import { rootStore } from '@/stores/rootStore';

export default {
    extends: OnEvent,
    props: {
        propValue: {
            type: Object,
            default: () => ({
                value: '',
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
    align-items: baseline;
    .input-textarea {
        width: 100%;
        height: 100%;
    }
}
</style>
