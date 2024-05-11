<template>
    <div class="input-wrap">
        <el-input class="input-textarea" v-model="value" size="small" type="textarea" />
    </div>
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
