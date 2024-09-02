<template>
    <div v-if="editMode == 'edit'" class="v-tabs">
        <el-tabs 
            v-model="activeName" 
            :tab-position="element.position" 
            type="border-card" 
            @tab-click="handleClick"
        >
            <el-tab-pane 
                v-for="tab in element.tabs" 
                :key="tab.name" 
                :label="tab.label" 
                :name="tab.name"
                :disabled="tab.label === visibleName"
                class="use-tabs-active"
            >
                <Container
                    :element="element"
                    :name="tab.name"
                    :childs="childs.filter((i) => i.activeName === tab.name)"
                >
                </Container>
            </el-tab-pane>
        </el-tabs>
    </div>
    <div v-else class="v-tabs preview">
        <el-tabs 
            v-model="activeName" 
            :tab-position="element.position" 
            type="border-card" 
            @tab-click="handleClick"
        >
            <el-tab-pane 
                v-for="tab in element.tabs" 
                :key="tab.name" 
                :label="tab.label" 
                :name="tab.name"
                :disabled="tab.label === visibleName"
            >
                <PreviewContainer
                    :element="element"
                    :name="tab.name"
                    :childs="childs.filter((i) => i.activeName === tab.name)"
                />
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import { keycodes } from '@/utils/shortcutKey.js';
import Container from '../common/Container.vue';
import PreviewContainer from '../common/PreviewContainer.vue';
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet } from '@/utils/utils';

export default {
    components: {
        Container,
        PreviewContainer,
    },
    props: {
        propValue: {
            type: Object,
            default: () => ({
                visibleName: 'visibleName',
                autoActiveName: "autoActiveName"
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
            activeName: null,
        };
    },
    computed: {
        visibleName: {
            get() {
                return getComputedGet('visibleName', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('visibleName', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        autoActiveName: {
            get() {
                return getComputedGet('autoActiveName', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('autoActiveName', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        editMode () {
            return rootStore.editor.editMode
        },
        componentData() {
            return rootStore.dataCenter.componentData;
        },
        childs() {
            return this.componentData.filter((i) => i.pid === this.element.id);
        },
    },
    mounted() {
        if (this.element.tabs && this.element.tabs.length) {
            this.activeName = this.element.tabs[0].name;
            if (this.autoActiveName === 'OFDM 网格' || this.autoActiveName === '星座图') {
                this.activeName = this.element.tabs.find((i) => i.label === this.autoActiveName)?.name;
            }
        }
    },
    methods: {
        handleClick(e) {
            const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'updateValue');
            if (linkageEvents.length) {
                eventBus.$emit('updateValue', linkageEvents, e.label);
            }
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
            this.element.propValue = e.target.innerHTML || '&nbsp;';
            const html = e.target.innerHTML;
            if (html !== '') {
                this.element.propValue = e.target.innerHTML;
            } else {
                this.element.propValue = '';
                this.$nextTick(() => {
                    this.element.propValue = '&nbsp;';
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
    watch: {
        autoActiveName(val) {
            if (val === 'OFDM 网格' || val === '星座图') {
                this.activeName = this.element.tabs.find((i) => i.label === val)?.name;
            }
        },
    },
};
</script>

<style lang="less" scoped>
.preview {
    user-select: none;
}
</style>
