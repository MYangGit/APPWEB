<!-- eslint-disable vue/no-v-html -->
<template>
    <div v-if="editMode == 'edit'" class="v-tabs">
        <FlexContainer
            :flexOptions="{
                direction,
                horAlign,
                verAlign,
                wrapType
            }"
            :element="element"
            :name="element.id"
            :childs="childs"
        >
        </FlexContainer>
    </div>
    <div v-else class="v-tabs preview">
        <PreviewContainer
            :flexOptions="{
                direction,
                horAlign,
                verAlign,
                wrapType
            }"
            layoutType="flex"
            :element="element"
            :name="element.id"
            :childs="childs"
        />
    </div>
</template>

<script>
import FlexContainer from '../common/FlexContainer.vue';
import PreviewContainer from '../common/PreviewContainer.vue';
import OnEvent from '../common/OnEvent';
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet } from '@/utils/utils';

export default {
    components: {
        FlexContainer,
        PreviewContainer,
    },
    extends: OnEvent,
    props: {
        propValue: {
            type: Object,
            default: () => {}
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
        direction: {
            get() {
                return getComputedGet('direction', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('direction', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        horAlign: {
            get() {
                return getComputedGet('horAlign', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('horAlign', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        verAlign: {
            get() {
                return getComputedGet('verAlign', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('verAlign', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        wrapType: {
            get() {
                return getComputedGet('wrapType', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('wrapType', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        editMode () {
            return rootStore.editor.editMode
        },
        childs() {
            return rootStore.dataCenter.componentData.filter((i) => i.pid === this.element.id);
        },
    },
    mounted() {
    }
};
</script>

<style lang="less" scoped>
.preview {
    user-select: none;
}
</style>
