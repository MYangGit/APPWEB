<template>
    <div class="input-wrap">
        <erFormItem :label="label" >
            <erInput 
                :placeholder="Placeholder"
                :disabled="disabled"
                :type="type" 
                :val="value"
                @onChangeValue="value = $event"
                @change="handleValueChange"
            />
        </erFormItem>
    </div>
</template>

<script>
import eventBus from '@/utils/eventBus';
import OnEvent from '../../common/OnEvent'
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet } from '@/utils/utils';
import { erFormItem, erInput } from 'errantia';
import { useEventCentre } from '@/hooks/useEventCentre';

const { onChange } = useEventCentre();
export default {
    extends: OnEvent,
    components: {
        erFormItem,
        erInput,
    },
    props: {
        propValue: {
            type: Object,
            default: () => ({
                disabled: false,
                Placeholder: '',
                type: 'text',
                label: '',
                value: '',
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    methods: {
        handleValueChange() {
            onChange({element: this.element, newValue: this.value})
        },
    },
    computed: {
        Placeholder: {
            get() {
                return getComputedGet('Placeholder', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('Placeholder', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
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
        label: {
            get() {
                return getComputedGet('label', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('label', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        type: {
            get() {
                return getComputedGet('type', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('type', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        value: {
            get() {
                return getComputedGet('value', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('value', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        }
    },
    watch: {
        propValue: {
            handler(val) {
                const linkageEvents = this.element.linkage.data.filter((i) => i.event === 'updateValue');
                if (linkageEvents.length) {
                    eventBus.$emit('updateValue', linkageEvents, { ...val });
                }
            },
            deep: true,
            immediate: true,
        },
    },
}
</script>

<style lang="less" scoped>
.input-wrap {
    display: inline-flex;
    align-items: center;
    label {
        word-break: keep-all;
        white-space: nowrap;
    }
}
</style>
