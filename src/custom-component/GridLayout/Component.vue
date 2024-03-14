<!-- eslint-disable vue/no-v-html -->
<template>
    <div
        v-if="editMode == 'edit'"
        class="v-grid"
        :style="{ 'grid-template-columns': `repeat(${element.cols}, 1fr)`, 'grid-template-rows': `repeat(${element.rows}, 1fr)` }"
    >
        <div v-for="(item, index) in element.items" :key="index" class="border">
            <Container :element="element" :name="item.name" :childs="childs.filter((i) => i.activeName === item.name)"></Container>
        </div>
    </div>
    <div
        v-else
        class="v-grid preview"
        :style="{ 'grid-template-columns': `repeat(${element.cols}, 1fr)`, 'grid-template-rows': `repeat(${element.rows}, 1fr)` }"
    >
        <div v-for="(item, index) in element.items" :key="index">
            <PreviewContainer :element="element" :name="item.name" :childs="childs.filter((i) => i.activeName === item.name)" />
        </div>
    </div>
</template>

<script>
import { mapState } from 'pinia'
import { keycodes } from '@/utils/shortcutKey.js'
import Container from '../common/Container.vue'
import PreviewContainer from '../common/PreviewContainer.vue'
import OnEvent from '../common/OnEvent'
import { rootStore } from '@/stores/rootStore'

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
        }
    },
    computed: {
        ...mapState(rootStore.useEditorStore, ['editMode']),
        ...mapState(rootStore.useDataCenterStore, ['componentData']),
        childs() {
            return this.componentData.filter((i) => i.pid === this.element.id)
        },
    },
    mounted() {
        if (this.element.tabs) {
            this.activeName = this.element.tabs[0].name
        }
    },
    methods: {
        handleClick(e) {
            console.log(e)
        },

        handleKeydown(e) {
            // 阻止冒泡，防止触发复制、粘贴组件操作
            this.canEdit && e.stopPropagation()
            if (e.keyCode == this.ctrlKey) {
                this.isCtrlDown = true
            } else if (this.isCtrlDown && this.canEdit && keycodes.includes(e.keyCode)) {
                e.stopPropagation()
            } else if (e.keyCode == 46) {
                // deleteKey
                e.stopPropagation()
            }
        },

        handleKeyup(e) {
            // 阻止冒泡，防止触发复制、粘贴组件操作
            this.canEdit && e.stopPropagation()
            if (e.keyCode == this.ctrlKey) {
                this.isCtrlDown = false
            }
        },

        handleMousedown(e) {
            if (this.canEdit) {
                e.stopPropagation()
            }
        },

        clearStyle(e) {
            e.preventDefault()
            const clp = e.clipboardData
            const text = clp.getData('text/plain') || ''
            if (text !== '') {
                document.execCommand('insertText', false, text)
            }

            this.$emit('input', this.element, e.target.innerHTML)
        },

        handleBlur(e) {
            this.element.propValue = e.target.innerHTML || '&nbsp;'
            const html = e.target.innerHTML
            if (html !== '') {
                this.element.propValue = e.target.innerHTML
            } else {
                this.element.propValue = ''
                this.$nextTick(() => {
                    this.element.propValue = '&nbsp;'
                })
            }
            this.canEdit = false
        },

        setEdit() {
            if (this.element.isLock) return

            this.canEdit = true
            // 全选
            this.selectText(this.$refs.text)
        },

        selectText(element) {
            const selection = window.getSelection()
            const range = document.createRange()
            range.selectNodeContents(element)
            selection.removeAllRanges()
            selection.addRange(range)
        },
    },
}
</script>

<style lang="less" scoped>
.v-grid {
    display: grid;
    grid-gap: 5px;
    padding: 5px;
}

.preview {
    user-select: none;
}

.border {
    border: 1px dashed #ccc;
}
</style>
