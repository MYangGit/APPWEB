<!-- eslint-disable vue/no-v-html -->
<template>
    <div
        class="v-grid"
        :style="{ 
            'grid-auto-flow': `${propValue.autoFlowRow ? 'row' : 'column'}`,
            'grid-column-gap': `${propValue.cgap}px`, 
            'grid-row-gap': `${propValue.rgap}px`, 
            'grid-template-columns': `repeat(${cols}, 1fr)`, 
            'grid-template-rows': `repeat(${rows}, 1fr)` 
        }"
    >
        <div 
            v-for="item in gridItems" 
            :key="item.name" 
            v-show="item.visible"
            :style="{ 'grid-column-end': `span ${item.cSpan}`, 'grid-row-end': `span ${item.rSpan}`}"
        >
            <div 
                v-if="editMode == 'edit'" 
                class="border"
                style="width: 100%; height: 100%;"
            > 
                <Container
                    :element="element"
                    :name="element.items?.filter((i) => i.label === item.name)[0].name"
                    :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label === item.name)[0].name)"
                />
            </div>
            <div 
                v-else 
                style="width: 100%; height: 100%;" 
                class="preview"
            >
                <PreviewContainer
                    :element="element"
                    :name="element.items?.filter((i) => i.label === item.name)[0].name"
                    :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label === item.name)[0].name)"
                />
            </div>
        </div>
    </div>
</template>

<script>
import Container from '../../common/Container.vue';
import PreviewContainer from '../../common/PreviewContainer.vue';
import OnEvent from '../../common/OnEvent';
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet } from '@/utils/utils';

export default {
    components: {
        Container,
        PreviewContainer,
    },
    extends: OnEvent,
    props: {
        propValue: {
            type: Object,
            default: () => ({
                autoFlowRow: true,
                cgap: 5,
                rgap: 5,
                cols: 2,
                rows: 2,
                gridItems: [
                    {
                        name: 'ErGrid1',
                        visible: true,
                        cSpan: 1,
                        rSpan: 1,
                    },
                    {
                        name: 'ErGrid2',
                        visible: true,
                        cSpan: 1,
                        rSpan: 1,
                    },
                ]
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    data() {
        return {
        };
    },
    computed: {
        editMode () {
            return rootStore.editor.editMode
        },
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
        childs() {
            return rootStore.dataCenter.componentData.filter((i) => i.pid === this.element.id);
        },
        cols: {
            get() {
                return getComputedGet('cols', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('cols', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        rows: {
            get() {
                return getComputedGet('rows', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('rows', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        gridItems: {
            get() {
                return getComputedGet('gridItems', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('gridItems', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
    },
    mounted() {
    },
    methods: {
    },
};
</script>

<style lang="less" scoped>
.v-grid {
    display: grid;
}
.preview {
    user-select: none;
}
.border {
    border: 1px dashed #ccc;
} 
</style>
