<template>
    <div :style="displaySrcUseCss(srcPath)">
       <img 
        v-if="!isEmpty(srcPath) && !cssBg"
        class="resource-show"
        :src="displaySrc(srcPath)"
       >
    </div>
</template>

<script>
import { getComputedGet, getComputedSet, isEmpty} from '../../../utils/utils'
import { rootStore } from '@/stores/rootStore';
import { WIRELESS, Radar  } from '@/assets/AppResources/index.js';

const useIconS = {
    wireless: WIRELESS,
    radar: Radar
}
export default {
    props: {
        propValue: {
            type: Object,
            default: () => ({
                srcPath: '',
                base64: false,
                cssBg: false
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
        cssBg: {
            get() {
                return getComputedGet('cssBg', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('cssBg', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
    },
    methods:{
        isEmpty,
        displaySrc(srcPath) {
            if (srcPath.startsWith('http')) {
                return srcPath
            }
            if (this.base64) {
                return `data:image/png;base64,${srcPath}`
            }
            // 内部icon
            const iconPathArr = srcPath.split('.')
            if (iconPathArr.length === 2) {
                return useIconS[iconPathArr[0]] ? useIconS[iconPathArr[0]][iconPathArr[1]] : srcPath
            }
            return srcPath 
        },
        displaySrcUseCss(srcPath) {
            if (this.cssBg) {
                let cssPath = srcPath
                if (this.base64) {
                    cssPath = `data:image/png;base64,${srcPath}`
                }
                return {
                    backgroundImage: `url(${cssPath})`,
                    backgroundRepeat: 'no-repeat',
                    backgroundSize: 'cover',
                    backgroundPosition: '50% center',
                    width: '100%'
                }
            }
            return {}
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
