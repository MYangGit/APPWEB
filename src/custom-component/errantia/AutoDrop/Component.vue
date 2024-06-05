<!-- eslint-disable vue/no-v-html -->
<template>
    <div class="input-wrap">
        <el-dropdown 
            ref="dropdown1" 
            :trigger="propValue.trigger"
            @command="handleCommand"
        >
            <div :class="{activate: isEmpty(activateText) ? activate : activate == activateText, disabledClick: disabled }" class="dropdown-title" >
                <div :style="{ width: element.style.width + 'px', height: element.style.height + 'px'}">
                    <div v-if="editMode == 'edit'" style="width: 100%; height: 100%;">
                        <Container
                            :element="element"
                            :name="element.id"
                            :childs="childs"
                        >
                        </Container>
                    </div>
                    <div v-else style="width: 100%; height: 100%;" class="preview">
                        <PreviewContainer
                            :element="element"
                            :name="element.id"
                            :childs="childs"
                        />
                    </div>
                </div>
            </div>
            <template #dropdown>
                <div :style="{ width: propValue.floatWidth + 'px', height: propValue.floatHeight + 'px'}">
                    <el-dropdown-menu>
                        <el-dropdown-item 
                            v-for="item in dropdownMenu" 
                            :key="item.command" 
                            :command="item.command"
                            :disabled="item.disabled"
                            :divided="item.divided"
                        >
                            {{ item.name }}
                        </el-dropdown-item>
                    </el-dropdown-menu>
                </div>
            </template>
        </el-dropdown>
    </div> 
</template>

<script>
import Container from '../../common/Container.vue';
import PreviewContainer from '../../common/PreviewContainer.vue';
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet, isEmpty } from '@/utils/utils';
import { useEventCentre } from '@/hooks/useEventCentre';

const { onClickOther } = useEventCentre();
export default {
    components: {
        Container,
        PreviewContainer,
    },
    props: {
        propValue: {
            type: Object,
            default: () => ({
                titleWidth: 200,
                titleHeight: 200,
                disabled: false,
                activate: false,
                activateText: '',
                trigger: 'contextmenu',
                floatHeight: 200,
                floatWidth: 200,
                dropdownMenu: [
                    { name: 'Action 1', command: 'a', disabled: false, divided: false},
                ]
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
        disabled: {
            get() {
                return getComputedGet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        dropdownMenu: {
            get() {
                return getComputedGet('dropdownMenu', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('dropdownMenu', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
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
    },
    methods: {
        isEmpty,
        handleCommand(command) {
            onClickOther({element: this.element, clickName: 'clickCommand', params: { command }})
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
.disabledClick {
    cursor: not-allowed;    
    pointer-events: none;
    background-color: #f5f7fa;
}
.activate {
    cursor: pointer;
    background-color: #cbe8fe;
    border-radius: 4px;
}
.dropdown-title {
    text-align: center;
    cursor: pointer;
}
</style>
