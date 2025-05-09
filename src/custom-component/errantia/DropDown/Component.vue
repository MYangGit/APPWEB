<!-- eslint-disable vue/no-v-html -->
<template>
    <div class="input-wrap">
        <div style="height: 100%;" :class="{activateStyle: isActivated, disabledClick: disabled}">
            <el-dropdown 
                ref="dropdown1" 
                :trigger="propValue.trigger"
            >
                <div class="dropdown-title" :style="{ width: propValue.titleWidth + 'px'}">
                    <erPicText
                        :disabled="disabled"
                        :hasSubscript="propValue.hasSubscript"
                        :horizontal="propValue.horizontal"
                        :iconPath="useIcon(propValue.iconPath)"
                        :title="title"
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
                        <div @contextmenu.prevent v-if="editMode == 'edit'" style="width: 100%; height: 100%;" class="v-tabs">
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
    </div>
</template>

<script>
import Container from '../../common/Container.vue';
import PreviewContainer from '../../common/PreviewContainer.vue';
import { rootStore } from '@/stores/rootStore';
import { erPicText } from 'errantia';
import { getComputedGet, getComputedSet, isEmpty } from '@/utils/utils';
import { useEventCentre } from '@/hooks/useEventCentre';
import { WIRELESS, Radar  } from '@/assets/AppResources/index.js';
import { useUtilsCentre } from '@/hooks/useUtilsCentre';
const useIconS = {
    wireless: WIRELESS,
    radar: Radar
}
const { onClickOther } = useEventCentre();
const { disablePro } = useUtilsCentre();
export default {
    components: {
        Container,
        PreviewContainer,
        erPicText
    },
    props: {
        propValue: {
            type: Object,
            default: () => ({
                disabledText: '',
                title: '标题',
                titleWidth: 100,
                disabled: false,
                activate: false,
                activateText: '',
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
        return {};
    },
    computed: {
        title: {
            get() {
                return getComputedGet('title', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('title', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        disabled: {
            get() {
                let disVal =  getComputedGet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
                return disablePro(disVal, this.propValue?.disabledText)
            },
            set(val) {
                getComputedSet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        activate: {
            get() {
                return getComputedGet('activate', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('activate', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        activateText: {
            get() {
                return getComputedGet('activateText', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('activateText', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        editMode () {
            return rootStore.editor.editMode
        },
        childs() {
            return rootStore.dataCenter.componentData.filter((i) => i.pid === this.element.id);
        },
        isActivated() {
            return this.isEmpty(this.activateText) ? this.activate : this.activate == this.activateText
        },
    },
    methods: {
        isEmpty,
        handleAction(val) {
            val.e.stopPropagation();
            const { activateText } = this;
            onClickOther({element: this.element, clickName: 'click', params: { val, activateText }})
        },
        onContextMenu() {
            this.showClick()
        },
        showClick() {
            if (!this.$refs.dropdown1) return
            if(this.isShowVisible) {
                this.$refs.dropdown1.handleClose()
            } else {
                this.$refs.dropdown1.handleOpen()
            }
        },
        useIcon(iconPath) {
            if (iconPath.startsWith('http')) {
                return iconPath
            }
            const iconPathArr = iconPath.split('.')
            if (iconPathArr.length === 2) {
                return useIconS[iconPathArr[0]] ? useIconS[iconPathArr[0]][iconPathArr[1]] : iconPath
            }
            return iconPath
        }
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
.disabledClick {
    cursor: not-allowed;    
    pointer-events:none;
}
.activateStyle {
    cursor: pointer;
    background-color: #cbe8fe;
    border-radius: 4px;
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
