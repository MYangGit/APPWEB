<template>
    <div>
       <img 
        v-if="!isEmpty(srcPath)"
        class="resource-show"
        :src="displaySrc(srcPath)"
       >
    </div>
</template>

<script>
import { getComputedGet, getComputedSet, isEmpty} from '../../../utils/utils'
import { rootStore } from '@/stores/rootStore';


export default {
    props: {
        propValue: {
            type: Object,
            default: () => ({
                srcPath: '',
                base64: false,
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    computed: {
        srcPath: {
            get() {
                return getComputedGet('srcPath', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('srcPath', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        base64: {
            get() {
                return getComputedGet('base64', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('base64', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
    },
    methods:{
        isEmpty,
        displaySrc(srcPath) {
            console.log('srcPath', srcPath)
            if (srcPath.startsWith('http')) {
                return srcPath
            }
            if (this.base64) {
                return `data:image/png;base64,${srcPath}`
            }
            return srcPath
        }
    }
}
</script>

<style lang="less" scoped>
.resource-show {
    width: 100%;
    height: 100%;
    object-fit: contain;
}
</style>
