<!-- eslint-disable vue/no-v-html -->
<template>
    <div v-show="isShowVisible || propValue.showVisible" :class="{'erdialog-header': propValue.showDialogHeader, 'erdialog-footer': true}">
        <erDialog 
            :title="title"
            :width="propValue.width + 'px'"
            :outStyleBody="{height: propValue.height + 'px', flex: 'none'}"
            :isVisible="isShowVisible || propValue.showVisible"
            @close="isShowVisible = false"
        >
            <div v-if="editMode == 'edit'" style="width: 100%; height: 100%;" class="v-tabs">
                <Container
                    :element="element"
                    :name="element.id"
                    :childs="childs"
                >
                </Container>
            </div>
            <div v-else style="width: 100%; height: 100%;" class="v-tabs preview">
                <PreviewContainer
                    :element="element"
                    :name="element.id"
                    :childs="childs"
                />
            </div>
        </erDialog>
    </div>
</template>

<script>
import Container from '../../common/Container.vue';
import PreviewContainer from '../../common/PreviewContainer.vue';
import { getComputedGet, getComputedSet } from '@/utils/utils';
import { rootStore } from '@/stores/rootStore';
import { erDialog } from 'errantia';


export default {
    components: {
        Container,
        PreviewContainer,
        erDialog
    },
    props: {
        propValue: {
            type: Object,
            default: () => ({
                isShowVisible: false,
                showVisible: false,
                showDialogHeader: false,
                title: '弹窗',
                width: 400,
                height: 300,
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
        isShowVisible: {
            get() {
                return getComputedGet('isShowVisible', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('isShowVisible', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        title: {
            get() {
                return getComputedGet('title', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('title', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        }
    },
    methods: {
        
    }
};
</script>

<style lang="less" scoped>
.preview {
    user-select: none;
}
.erdialog-header {
    :deep(.dialog-header) {
        display: none !important;
    }
}
.erdialog-footer {
    :deep(.footer) {
        display: none !important;
    }
}
</style>
