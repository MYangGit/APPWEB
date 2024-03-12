<!-- eslint-disable vue/no-v-html -->
<template>
    <div v-if="editMode == 'edit'" class="v-tabs">
        <div
            ref="text"
            :contenteditable="canEdit"
            :class="{ canEdit }"
            :tabindex="element.id"
            :style="{ verticalAlign: element.style.verticalAlign }"
            @dblclick="setEdit"
            @paste="clearStyle"
            @mousedown="handleMousedown"
            @blur="handleBlur"
            @input="handleInput"
            v-html="element.propValue.text"
        ></div>
        <Container :element="element" :name="element.id" :childs="childs.filter((i) => i.activeName === element.id)">
        </Container>
    </div>
    <div v-else class="v-tabs preview">
        <div :style="{ verticalAlign: element.style.verticalAlign }" v-html="element.propValue.text"></div>
        <PreviewContainer
            :element="element"
            :name="element.id"
            :childs="childs.filter((i) => i.activeName === element.id)"
        />
    </div>
</template>

<script>
import { mapState } from 'vuex';
import { keycodes } from '@/utils/shortcutKey.js';
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
            type: Object,
            default: () => {},
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
        };
    },
    computed: {
        ...mapState(['editMode', 'componentData']),
        childs() {
            return this.componentData.filter((i) => i.pid === this.element.id);
        },
    },
    mounted() {},
    methods: {
        handleInput(e) {
            this.$emit('input', this.element, e.target.innerHTML);
        },
        handleClick(e) {
            console.log(e);
        },

        handleKeydown(e) {
            // 阻止冒泡，防止触发复制、粘贴组件操作
            this.canEdit && e.stopPropagation();
            if (e.keyCode == this.ctrlKey) {
                this.isCtrlDown = true;
            } else if (this.isCtrlDown && this.canEdit && keycodes.includes(e.keyCode)) {
                e.stopPropagation();
            } else if (e.keyCode == 46) {
                // deleteKey
                e.stopPropagation();
            }
        },

        handleKeyup(e) {
            // 阻止冒泡，防止触发复制、粘贴组件操作
            this.canEdit && e.stopPropagation();
            if (e.keyCode == this.ctrlKey) {
                this.isCtrlDown = false;
            }
        },

        handleMousedown(e) {
            if (this.canEdit) {
                e.stopPropagation();
            }
        },

        clearStyle(e) {
            e.preventDefault();
            const clp = e.clipboardData;
            const text = clp.getData('text/plain') || '';
            if (text !== '') {
                document.execCommand('insertText', false, text);
            }

            this.$emit('input', this.element, e.target.innerHTML);
        },

        handleBlur(e) {
            this.element.propValue.text = e.target.innerHTML || '&nbsp;';
            const html = e.target.innerHTML;
            if (html !== '') {
                this.element.propValue.text = e.target.innerHTML;
            } else {
                this.element.propValue.text = '';
                this.$nextTick(() => {
                    this.element.propValue.text = '&nbsp;';
                });
            }
            this.canEdit = false;
        },

        setEdit() {
            if (this.element.isLock) return;

            this.canEdit = true;
            // 全选
            this.selectText(this.$refs.text);
        },

        selectText(element) {
            const selection = window.getSelection();
            const range = document.createRange();
            range.selectNodeContents(element);
            selection.removeAllRanges();
            selection.addRange(range);
        },
    },
};
</script>

<style lang="less" scoped>
.preview {
    user-select: none;
}
</style>
