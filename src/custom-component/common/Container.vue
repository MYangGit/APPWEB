<template>
    <div
        :id="name"
        class="content"
        :class="isActiveContainer === name ? 'active' : ''"
        @drop="handleDrop"
        @dragover="handleDragOver"
        @click="handleClick"
    >
        <Shape
            v-for="(item, index) in childs"
            :key="item.id"
            :default-style="item.style"
            :style="getShapeStyle(item.style)"
            :active="item.id === (curComponent || {}).id"
            :element="item"
            :index="index"
            :class="{
                lock: item.isLock,
            }"
        >
            <component
                :is="item.component"
                v-if="item.component.startsWith('SVG')"
                :id="'component' + item.id"
                :style="getSVGStyle(item.style)"
                class="component"
                :prop-value="item.propValue"
                :element="item"
                :request="item.request"
                :linkage="item.linkage"
            />

            <component
                :is="item.component"
                v-else-if="item.component != 'VText'"
                :id="'component' + item.id"
                class="component"
                :style="getComponentStyle(item.style)"
                :prop-value="item.propValue"
                :element="item"
                :request="item.request"
                :linkage="item.linkage"
            />

            <component
                :is="item.component"
                v-else
                :id="'component' + item.id"
                class="component"
                :style="getComponentStyle(item.style)"
                :prop-value="item.propValue"
                :element="item"
                :request="item.request"
                :linkage="item.linkage"
                @input="handleInput"
            />
        </Shape>
    </div>
</template>

<script>
import { deepCopy } from '@/utils/utils';
import { mapState } from 'vuex';
import generateID from '@/utils/generateID';
import componentList from '@/custom-component/component-list'; // 左侧列表数据
import { getStyle, getShapeStyle, getSVGStyle, getCanvasStyle } from '@/utils/style';
import Shape from '../../components/Editor/Shape';

export default {
    name: 'Container',
    components: {
        Shape,
    },
    props: {
        propValue: {
            type: Array,
            default: () => [],
        },
        element: {
            type: Object,
            default: () => {},
        },
        name: {
            type: String,
            default: () => '1',
        },
        childs: {
            type: Array,
            default: () => [],
        },
    },
    data() {
        return {
            svgFilterAttrs: ['rotate'],
        };
    },
    computed: {
        ...mapState(['curComponent', 'isActiveContainer', 'canvasStyleData', 'componentData']),
    },
    methods: {
        getShapeStyle,
        getCanvasStyle,
        handleClick(e) {
            e.preventDefault();
            e.stopPropagation();
            this.$store.commit('setActiveContainer', this.name);
            const rectInfo = document.getElementById(this.name).getBoundingClientRect();
            const top = e.clientY - rectInfo.y;
            const left = e.clientX - rectInfo.x;
            this.$store.commit('setPosition', { top, left });
        },
        // 组件拖拽的动作
        handleDrop(e) {
            e.preventDefault();
            e.stopPropagation();
            const index = e.dataTransfer.getData('index');
            const rectInfo = document.getElementById(this.name).getBoundingClientRect();
            if (index) {
                const component = deepCopy(componentList[index]);
                component.style.top = e.clientY - rectInfo.y;
                component.style.left = e.clientX - rectInfo.x;
                if (component.type === 'report') {
                    component.style.left = 0;
                }
                component.id = generateID();
                component.pid = this.element.id;
                component.activeName = this.name;
                if (component.component === 'Tabs') {
                    component.tabs = new Array(3).fill(1).map((i, j) => ({
                        name: generateID(),
                        label: `Tab${j + 1}`,
                    }));
                } else if (component.component === 'GridLayout') {
                    component.items = new Array(3 * 3).fill(1).map((i, j) => ({
                        name: generateID(),
                        label: `Grid${j + 1}`,
                    }));
                }
                if (component.style.width.toString().includes('%')) {
                    component.style.width =
                        (Number(this.canvasStyleData.width) * parseFloat(component.style.width)) / 100;
                }
                if (this.componentData.filter(i => i.component === component.component).length) {
                    component.label += this.componentData.filter(i => i.component === component.component).length;
                }
                this.$store.commit('addComponent', { component });
                this.$store.commit('recordSnapshot');
            }
        },

        handleDragOver(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
            this.$store.commit('setActiveContainer', this.name);
        },

        handleMouseDown(e) {
            e.stopPropagation();
            this.$store.commit('setClickComponentStatus', false);
            this.$store.commit('setInEditorStatus', true);
        },
        deselectCurComponent(e) {
            if (!this.isClickComponent) {
                this.$store.commit('setCurComponent', {
                    component: null,
                    index: null,
                });
            }

            // 0 左击 1 滚轮 2 右击
            if (e.button != 2) {
                this.$store.commit('hideContextMenu');
            }
        },
        getComponentStyle(style) {
            return getStyle(style, this.svgFilterAttrs);
        },

        getSVGStyle(style) {
            return getSVGStyle(style, this.svgFilterAttrs);
        },

        handleInput(element, value) {
            // 根据文本组件高度调整 shape 高度
            this.$store.commit('setShapeStyle', {
                height: this.getTextareaHeight(element, value),
            });
        },

        getTextareaHeight(element, text) {
            let { lineHeight, fontSize, height } = element.style;
            if (lineHeight === '') {
                lineHeight = 1.5;
            }

            const newHeight = (text.split('<br>').length - 1) * lineHeight * fontSize;
            return height > newHeight ? height : newHeight;
        },
    },
};
</script>

<style lang="less" scoped>
.content {
    width: 100%;
    height: 100%;
    overflow: auto;
    position: relative;
}
.active {
    border: 1px solid #70c0ff;
    user-select: none;
    box-sizing: content-box;
}
</style>
