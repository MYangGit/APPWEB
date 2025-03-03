<template>
    <div :class="{disabledStyle: disabled, checkStyle: isActivated }"  >
        <div 
            class="v-button" 
            
            @click="handleAction"
        >
            {{ value }}
        </div>
    </div>
</template>

<script>
import { getComputedGet, getComputedSet, isEmpty } from '../../utils/utils'
import { rootStore } from '@/stores/rootStore';
import { useEventCentre } from '@/hooks/useEventCentre';

const { onClickOther } = useEventCentre();
export default {
    props: {
        propValue: {
            type: Object,
            default: () => ({
                value: '',
                disabled: false,
                activate: false,
                activateText: "",
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    computed: {
        value: {
            get() {
                return getComputedGet('value', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('value', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        disabled: {
            get() {
                return getComputedGet('disabled', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
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
        isActivated() {
            return this.isEmpty(this.activateText) ? this.activate : this.activate == this.activateText
        },
    },
    methods: {
        isEmpty,
        handleAction(e) {
            e.stopPropagation();
            const { value, activateText, activate } = this;
            onClickOther({element: this.element, clickName: 'click', params: { name: value, activateText, activate }})
        },
    },
}
</script>

<style lang="less" scoped>
.v-button {
    display: flex;
    align-items: center;
    justify-content: center;
    white-space: nowrap;
    cursor: pointer;
    box-sizing: border-box;
    outline: 0;
    margin: 0;
    transition: .1s;
    width: 100%;
    height: 100%;
    &:active {
        color: #3a8ee6;
        border-color: #3a8ee6;
        outline: 0;
    }
    &:hover {
        background-color: #ecf5ff;
        color: #3a8ee6;
    }
}
.disabledStyle {
    cursor: not-allowed;
    background-color: #f5f7fa;
    color: #c0c4cc;
    border-color: #ebeef5 !important;
    pointer-events: none;
}
.checkStyle {
    color: #3a8ee6 !important;
    border-color: #3a8ee6 !important;
}
</style>
