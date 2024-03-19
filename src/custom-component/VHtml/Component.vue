<template>
    <div ref="htmlhost" class="v-html"></div>
</template>

<script>
import OnEvent from '../common/OnEvent'
import { getComputedGet, getComputedSet } from '../../utils/utils'
import { rootStore } from '@/stores/rootStore';

export default {
    extends: OnEvent,
    props: {
        propValue: {
            type: Object,
            default: () => {},
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    data() {
        return {
            shadow: null,
        }
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
    },
    watch: {
        'value': {
            handler(val) {
                this.shadow.innerHTML = this.value;
            }
        },
    },
    mounted() {
        this.shadow = this.$refs.htmlhost.attachShadow({ mode: 'open' });
        if (this.propValue) {
            this.shadow.innerHTML = this.value;
        }
    },
}
</script>

<style lang="less" scoped>
.v-html {
    border: 1px solid transparent;
    overflow: auto;
}
</style>
