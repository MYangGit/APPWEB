<!-- eslint-disable vue/no-v-html -->
<template>
    <div 
        v-if="editMode == 'edit'" 
        class="v-tabs"
        :style="displaySrcUseCss(srcPath)"
    >
        <Container
            :element="element"
            :name="element.id"
            :childs="childs"
        >
        </Container>
    </div>
    <div 
        v-else 
        class="v-tabs preview"
        :style="displaySrcUseCss(srcPath)"
    >
        <PreviewContainer
            :element="element"
            :name="element.id"
            :childs="childs"
        />
    </div>
</template>

<script>
import Container from '../common/Container.vue';
import PreviewContainer from '../common/PreviewContainer.vue';
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet, isEmpty} from '../../utils/utils'

export default {
    components: {
        Container,
        PreviewContainer,
    },
    props: {
        propValue: {
            type: Object,
            default: () => ({
                srcPath: '',
                cutAndCover: false,
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
        linkage: {
            type: Object,
            default: () => {},
        },
    },
    data() {
        return {
            canEdit: false,
            ctrlKey: 17,
            isCtrlDown: false,
            cancelRequest: null,
            activeName: null,
        };
    },
    computed: {
        editMode () {
            return rootStore.editor.editMode
        },
        childs() {
            return rootStore.dataCenter.componentData.filter((i) => i.pid === this.element.id);
        },
        srcPath: {
            get() {
                return getComputedGet('srcPath', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('srcPath', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
    },
    methods: {
        isEmpty,
        displaySrcUseCss(srcPath) {
            if (!isEmpty(srcPath)) {
                if( this.propValue.cutAndCover){
                    return {
                        backgroundImage: `url(${srcPath})`,
                        backgroundRepeat: 'no-repeat',
                        backgroundSize: 'cover',
                        backgroundPosition: 'center center',
                    }
                }
                return {
                    backgroundImage: `url(${srcPath})`,
                    backgroundRepeat: 'no-repeat',
                    backgroundSize: 'contain',
                    backgroundPosition: 'center center',
                }
            }
            return {}
        }
    },
};
</script>

<style lang="less" scoped>
.preview {
    user-select: none;
}
</style>
