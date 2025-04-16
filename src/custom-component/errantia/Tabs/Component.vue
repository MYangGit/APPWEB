<template>
    <div v-if="editMode == 'edit'">
        <el-tabs 
            style="border: none;"
            v-model="autoActiveName" 
            :tab-position="element.position" 
            type="border-card" 
            @tab-remove="handleRemove"
            @tab-click="handleClick"
        >
            <el-tab-pane 
                v-for="tab in tabsItem?.filter((i) => i.visible)" 
                :key="tab.name" 
                :label="tab.label" 
                :name="tab.name"
                :closable="tab.closable"
                :disabled="tab.disabled"
            >
                <Container
                    :element="element"
                    :name="element.items?.filter((i) => i.label === displayContent(tab.name))[0].name"
                    :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label ===displayContent(tab.name))[0].name)"
                />
            </el-tab-pane>
        </el-tabs>
    </div>
    <div v-else class="preview">
        <el-tabs 
            style="border: none;"
            v-model="autoActiveName" 
            :tab-position="element.position" 
            type="border-card"
            @tab-remove="handleRemove"
            @tab-click="handleClick"
        >
            <el-tab-pane 
                v-for="tab in tabsItem?.filter((i) => i.visible)" 
                :key="tab.name" 
                :label="tab.label" 
                :name="tab.name"
                :closable="tab.closable"
                :disabled="tab.disabled"
                :params="tab.params"
            >
                <PreviewContainer
                    :element="element"
                    :name="element.items?.filter((i) => i.label === displayContent(tab.name))[0].name"
                    :childs="childs.filter((i) => i.activeName === element.items?.filter((i) => i.label === displayContent(tab.name))[0].name)"
                />
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import Container from '../../common/Container.vue';
import PreviewContainer from '../../common/PreviewContainer.vue';
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet, isEmpty} from '@/utils/utils';
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
                fixed: "",
                activateText: "",
                tabsItem: [
                    {
                        name: 'ErTabs1',
                        label: 'ErTabs1',
                        closable: false,
                        disabled: false,
                        visible: true,
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
            activeName: 'ErTabs1',
        };
    },
    computed: {
        fixed: {
            get() {
                return getComputedGet('fixed', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('fixed', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        autoActiveName: {
            get() {
                if (this.tabsItem?.filter((i) => i.visible).length === 1) {
                    return this.tabsItem.filter((i) => i.visible)[0].name;
                }
                return this.activeName;
            },
            set(newValue) {
                this.activeName = newValue;
            }
        },
        tabsItem: {
            get() {
                return getComputedGet('tabsItem', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('tabsItem', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
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
        componentData() {
            return rootStore.dataCenter.componentData;
        },
        childs() {
            return rootStore.dataCenter.componentData.filter((i) => i.pid === this.element.id);
        },
    },
    methods: {
        isEmpty,
        displayContent(name){
            const fixed = this.fixed ?? this.propValue.fixed
            if (!this.isEmpty(fixed)) {
                const fixedVal = this.tabsItem?.filter((i) => i.name === fixed);
                if (fixedVal.length === 1) {
                    return fixedVal[0].name;
                }
            }
            return name
        },
        handleRemove(name) {
            const index = this.tabsItem.findIndex((i) => i.name === name);
            this.tabsItem[index].visible = false;
            this.activeName = this.tabsItem[0].name;
        },
        handleClick(tab) {
            const params = this.tabsItem.filter((i) => i.name === tab.props.name)[0].params;
            onClickOther({element: this.element, clickName: 'onClickTab', params: { nameItem : {...tab.props, params}, activeName: this.activeName, activateText: this.activateText }})
        },
    },
};
</script>

<style lang="less" scoped>
.preview {
    user-select: none;
}
</style>
