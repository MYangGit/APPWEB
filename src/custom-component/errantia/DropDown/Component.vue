<!-- eslint-disable vue/no-v-html -->
<template>
    <div class="input-wrap">
        <el-dropdown 
            ref="dropdown1" 
            :trigger="propValue.trigger"
            :disabled="propValue.disabled"
            @visible-change="handleVisible2"
        >
            <div class="dropdown-title" :style="{ width: propValue.titleWidth + 'px'}">
                <erPicText
                    :hasSubscript="propValue.hasSubscript"
                    :horizontal="propValue.horizontal"
                    :iconPath="propValue.iconPath"
                    :title="propValue.title"
                    @onAction="handleAction"
                    @onContextMenu="onContextMenu"
                />
            </div>
            <template #dropdown>
                <div 
                    :class="{'dropdown-content': propValue.marginLeft !== 0, hideOrgin: propValue.marginLeft !== 0}"
                    :style="{
                        width: propValue.floatWidth + 'px',
                        height: propValue.floatHeight + 'px',
                        marginLeft: propValue.marginLeft + 'px'
                    }"
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
                </div>
            </template>
        </el-dropdown>
    </div> 
</template>

<script>
import Container from '../../common/Container.vue';
import PreviewContainer from '../../common/PreviewContainer.vue';
import OnEvent from '../../common/OnEvent';
import { rootStore } from '@/stores/rootStore';
import { erPicText } from 'errantia';


export default {
    components: {
        Container,
        PreviewContainer,
        erPicText
    },
    extends: OnEvent,
    props: {
        propValue: {
            type: Object,
            default: () => ({
                title: '标题',
                titleWidth: 100,
                disabled: false,
                iconPath: 'https://img.icons8.com/ios/452/plus-math.png',
                trigger: 'click',
                floatHeight: 200,
                floatWidth: 200,
                horizontal: true,
                hasSubscript: true,
                marginLeft: 0,
            }),
        },
        element: {
            type: Object,
            default: () => {},
        }
    },
    data() {
        return {
            isShowVisible: false,
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
        handleAction(val) {
            console.log(val)
        },
        onContextMenu() {
            this.showClick()
        },
        handleVisible2(visible) {
            this.isShowVisible = visible
        },
        showClick() {
            if (!this.$refs.dropdown1) return
            if(this.isShowVisible) {
                this.$refs.dropdown1.handleClose()
            } else {
                this.$refs.dropdown1.handleOpen()
            }
        },
    }
};
</script>

<style lang="less" scoped>
.preview {
    user-select: none;
}
.input-wrap {
    display: inline-flex;
    align-items: center;
    label {
        word-break: keep-all;
        white-space: nowrap;
        margin-bottom: 0;
    }
}
.dropdown-title {
    text-align: center;
    cursor: pointer;
}
.dropdown-content{
    background: var(--el-bg-color-overlay);
    border: 1px solid var(--el-border-color-light);
    box-shadow: var(--el-dropdown-menu-box-shadow);
}
.hideOrgin{
    :deep(.el-dropdown__popper.el-popper){
        border: none; 
        box-shadow: none;
        background: none;
    }
    :deep(.el-popper.is-light){
        background: none;
        border: none;
    }
}
</style>
