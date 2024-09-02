<!-- eslint-disable vue/no-v-html -->
<template>
    <div :class="{'layout-css': editMode == 'edit' || !isEmpty(element.style.fixedHeight) }">
        <erLayout
            :outStyleHeader="{
                height: propValue.showHeader ? `${propValue.heightHeader}px`: '0px',
                backgroundColor: propValue.headerColor,
            }"
            :outStyleLeftSidebar="{
                width: `${propValue.widthLeftSidebar}px`,
                backgroundColor: propValue.leftSidebarColor,
            }"
            :outStyleRightSidebar="{
                width: `${propValue.widthRightSidebar}px`,
                backgroundColor: propValue.rightSidebarColor,
            }"
            :outStyleFooter="{
                height: `${propValue.heightFooter}px`,
                backgroundColor: propValue.footerColor,
            }"
            :outStyleMain="{
                flex: 1,
                width: '100%',
                height: '100%',
                backgroundColor: propValue.mainColor,
            }"
            :showLeftSidebar="propValue.showLeftSidebar"
            :showRightSidebar="propValue.showRightSidebar"
            :showFooter="propValue.showFooter"
        >
            <template #header>
                <div v-if="editMode == 'edit'" style="width: 100%; height: 100%;" class="v-tabs">
                    <Container
                        :element="element"
                        :name="element.items?.filter((i) => i.label === 'ErLayoutheader')[0].name"
                        :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label === 'ErLayoutheader')[0].name)"
                    />
                </div>
                <div v-else class="v-tabs preview" style="width: 100%; height: 100%;">
                    <PreviewContainer
                        :element="element"
                        :name="element.items?.filter((i) => i.label === 'ErLayoutheader')[0].name"
                        :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label === 'ErLayoutheader')[0].name)"
                    />
                </div>
            </template>
            <template #leftSidebar>
                <div v-if="editMode == 'edit'" style="width: 100%; height: 100%;" class="v-tabs">
                    <Container
                        :element="element"
                        :name="element.items?.filter((i) => i.label === 'ErLayoutleftSidebar')[0].name"
                        :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label === 'ErLayoutleftSidebar')[0].name)"
                    />
                </div>
                <div v-else style="width: 100%; height: 100%;" class="v-tabs preview">
                    <PreviewContainer
                        :element="element"
                        :name="element.items?.filter((i) => i.label === 'ErLayoutleftSidebar')[0].name"
                        :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label === 'ErLayoutleftSidebar')[0].name)"
                    />
                </div>
            </template>
            <template #main>
                <div v-if="editMode == 'edit'" style="width: 100%; height: 100%;" class="v-tabs">
                    <Container
                        :element="element"
                        :name="element.items?.filter((i) => i.label === 'ErLayoutmain')[0].name"
                        :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label === 'ErLayoutmain')[0].name)"
                    />
                </div>
                <div v-else style="width: 100%; height: 100%;" class="v-tabs preview">
                    <PreviewContainer
                        :element="element"
                        :name="element.items?.filter((i) => i.label === 'ErLayoutmain')[0].name"
                        :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label === 'ErLayoutmain')[0].name)"
                    />
                </div>
            </template>
            <template #rightSidebar>
                <div v-if="editMode == 'edit'" style="width: 100%; height: 100%;" class="v-tabs">
                    <Container
                        :element="element"
                        :name="element.items?.filter((i) => i.label === 'ErLayoutrightSidebar')[0].name"
                        :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label === 'ErLayoutrightSidebar')[0].name)"
                    />
                </div>
                <div v-else style="width: 100%; height: 100%;" class="v-tabs preview">
                    <PreviewContainer
                        :element="element"
                        :name="element.items?.filter((i) => i.label === 'ErLayoutrightSidebar')[0].name"
                        :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label === 'ErLayoutrightSidebar')[0].name)"
                    />
                </div>
            </template>
            <template #footer>
                <div v-if="editMode == 'edit'" style="width: 100%; height: 100%;" class="v-tabs">
                    <Container
                        :element="element"
                        :name="element.items?.filter((i) => i.label === 'ErLayoutfooter')[0].name"
                        :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label === 'ErLayoutfooter')[0].name)"
                    />
                </div>
                <div v-else style="width: 100%; height: 100%;" class="v-tabs preview">
                    <PreviewContainer
                        :element="element"
                        :name="element.items?.filter((i) => i.label === 'ErLayoutfooter')[0].name"
                        :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label === 'ErLayoutfooter')[0].name)"
                    />
                </div>
            </template>
        </erLayout>
    </div>
</template>

<script>
import { isEmpty } from '@/utils/utils';
import Container from '../../common/Container.vue';
import PreviewContainer from '../../common/PreviewContainer.vue';
import { rootStore } from '@/stores/rootStore';
import { erLayout } from 'errantia';

export default {
    components: {
        Container,
        PreviewContainer,
        erLayout,
    },
    props: {
        propValue: {
            type: Object,
            default: () => ({
                showHeader: true,
                showLeftSidebar: true,
                showRightSidebar: true,
                showFooter: true,
                heightHeader: 100,
                widthLeftSidebar: 150,
                widthRightSidebar: 150,
                heightFooter: 30,
                headerColor: 'lightpink',
                leftSidebarColor: 'lightblue',
                mainColor: 'coral',
                rightSidebarColor: 'yellow',
                footerColor: 'wheat',
            }),
        },
        element: {
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
    },
    methods: {
        isEmpty,
    },
    mounted() {
        if (this.element.tabs) {
            this.activeName = this.element.tabs[0].name
        }
    },
};
</script>

<style lang="less" scoped>
.preview {
    user-select: none;
}
.layout-css {
    :deep(.layout-container) {
        height: 100%;
        width: 100%;
    }
}
</style>
