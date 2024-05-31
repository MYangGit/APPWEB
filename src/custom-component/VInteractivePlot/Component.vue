<template>
    <div>
        <img :src="useBase64(srcUrl)" style="width: 100%; height: 100%;"/>
    </div>
</template>

<script>
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet } from '@/utils/utils';

export default {
    props: {
        propValue: {
            type: Object,
            default: () => ({
                srcUrl: '',
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    data () {
        return {}
    },
    computed: {
        srcUrl: {
            get() {
                return getComputedGet('srcUrl', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('srcUrl', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
    },
    methods: {
        useBase64(srcUrl) {
            if (!srcUrl) return ''
            return `data:image/png;base64,${srcUrl}`
        }
    },
}
</script>

<style lang="less" scoped>
</style>
