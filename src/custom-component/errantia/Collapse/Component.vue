<!-- eslint-disable vue/no-v-html -->
<template>
    <div>
        <div class="collapse-content">
            <el-collapse
                v-model="propValue.activePanelName"
                :accordion="propValue.accordion"
                :class="{arrowPosition: propValue.arrowPosition === 'left', arrowNear: propValue.arrowNear}"
                @change="handleChange"
            >
                <el-collapse-item
                    v-for="item in panelLists"
                    :key="item.name"
                    :title="item.title"  
                    :name="item.name"
                    v-show="item.visible"
                >
                    <div :style="{width: '100%', height: item.height + 'px'}">
                        <div v-if="editMode == 'edit'" style="width: 100%; height: 100%;" class="v-tabs">
                            <Container
                                :element="element"
                                :name="element.items.filter((i) => i.label === `ErCollapse${item.name}`)[0].name"
                                :childs="childs.filter((i) => i.activeName === element.items.filter((i) => i.label === `ErCollapse${item.name}`)[0].name)"
                            />
                        </div>
                        <div v-else style="width: 100%; height: 100%;" class="v-tabs preview">
                            <PreviewContainer
                                :element="element"
                                :name="element.items.filter((i) => i.label === `ErCollapse${item.name}`)[0].name"
                                :childs="childs.filter((i) => i.activeName === element.items.filter((i) => i.label === `ErCollapse${item.name}`)[0].name)"
                            />
                        </div>
                    </div>
                </el-collapse-item>
            </el-collapse>
            <div style="flex-grow: 1;">
                <div v-if="editMode == 'edit'" style="width: 100%; height: 100%;" class="v-tabs">
                    <Container
                        :element="element"
                        :name="element.items.filter((i) => i.label === `ErCollapseonly`)[0]?.name"
                        :childs="childs.filter((i) => i.activeName === element.items.filter((i) => i.label === `ErCollapseonly`)[0]?.name)"
                    />
                </div>
                <div v-else style="width: 100%; height: 100%;" class="v-tabs preview">
                    <PreviewContainer
                        :element="element"
                        :name="element.items.filter((i) => i.label === `ErCollapseonly`)[0]?.name"
                        :childs="childs.filter((i) => i.activeName === element.items.filter((i) => i.label === `ErCollapseonly`)[0]?.name)"
                    />
                </div>
            </div>
        </div>
    </div> 
</template>

<script>
import Container from '../../common/Container.vue';
import PreviewContainer from '../../common/PreviewContainer.vue';
import { rootStore } from '@/stores/rootStore';
import { useEventCentre } from '@/hooks/useEventCentre';   
import { getComputedGet, getComputedSet } from '@/utils/utils';

const { onChange } = useEventCentre();
export default {
    components: {
        Container,
        PreviewContainer,
    },
    props: {
        propValue: {
            type: Object,
            default: () => ({
                accordion: true,
                arrowPosition: 'right',
                arrowNear: false,
                activePanelName: ['1'],
                panelLists: [
                    {
                        name: 1,
                        title: '面板1',
                        height: 100,
                        visible: true,
                    }
                ],
            }),
        },
        element: {
            type: Object,
            default: () => {},
        }
    },
    data() {
        return {
        };
    },
    computed: {
        editMode () {
            return rootStore.editor.editMode
        },
        childs() {
            return rootStore.dataCenter.componentData.filter((i) => i.pid === this.element.id);
        },
        panelLists: {
            get() {
                return getComputedGet('panelLists', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('panelLists', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
    },
    methods: {
        handleChange(val) {
            onChange({element: this.element, newValue: val})
        }
    },
};
</script>

<style lang="less" scoped>
.preview {
    user-select: none;
}
.collapse-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
}
.arrowPosition {
    :deep(.el-collapse-item__arrow) {
        order: -1;
        margin: 0;
        margin-right: 5px;
    }
}
.arrowNear {
    :deep(.el-collapse-item__arrow) {
        margin: 0;
        margin-left: 5px;
    }
}
</style>
