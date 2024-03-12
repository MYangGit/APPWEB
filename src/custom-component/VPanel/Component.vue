<!-- eslint-disable vue/no-v-html -->
<template>
    <div v-if="editMode == 'edit'" class="v-tabs">
        <Container
            :element="element"
            :name="element.id"
            :childs="childs"
        >
        </Container>
    </div>
    <div v-else class="v-tabs preview">
        <PreviewContainer
            :element="element"
            :name="element.id"
            :childs="childs"
        />
    </div>
</template>

<script>
import { mapState } from 'vuex';
import { keycodes } from '@/utils/shortcutKey.js';
import eventBus from '@/utils/eventBus';
import Container from '../common/Container.vue';
import PreviewContainer from '../common/PreviewContainer.vue';
import OnEvent from '../common/OnEvent';

export default {
    components: {
        Container,
        PreviewContainer,
    },
    extends: OnEvent,
    props: {
        propValue: {
            type: Array,
            default: () => [],
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
        ...mapState(['editMode', 'componentData']),
        childs() {
            return this.componentData.filter((i) => i.pid === this.element.id);
        },
    },
    mounted() {
    },
    methods: {

    },
};
</script>

<style lang="less" scoped>
.preview {
    user-select: none;
}
</style>
