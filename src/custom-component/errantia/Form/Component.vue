<template>
    <div class="form-group">
        <el-form
            class="auto-form-style"
            :label-position="labelPosition"
            :size="size"
        >
            <template v-if="!isEmpty(formData)" v-for="item of formData">
                <el-form-item v-if="item.type === 'input' || isEmpty(item.type)" :label="item.label">
                    <el-input
                        v-model="item.value"
                        :disabled="item.disabled"
                        :placeholder="item.placeholder"
                        @change="(newVal) => handleValueChange(newVal, item)"
                    />
                </el-form-item>
                <el-form-item v-if="item.type === 'select'" :label="item.label">
                    <el-select
                        v-model="item.value"
                        :disabled="item.disabled"
                        :placeholder="item.placeholder"
                        @change="(newVal) => handleValueChange(newVal, item)"
                    >
                        <template v-if="!isEmpty(item?.options)"  v-for="opt of item.options">
                            <el-option 
                                v-if="!isEmpty(opt.index)"
                                :label="`${opt.label}${opt.index}`" 
                                :value="opt.value" 
                            />
                            <el-option 
                                v-else
                                :label="opt.label" 
                                :value="opt.value" 
                            />
                        </template>
                    </el-select>
                </el-form-item>
                <el-form-item v-if="item.type === 'checkbox'" :label="item.label">
                    <el-checkbox 
                        v-model="item.value" 
                        :disabled="item.disabled"
                        @change="(newVal) => handleValueChange(newVal, item)"
                    />
                </el-form-item>
                <el-form-item v-show="['regular_map', 'table'].includes(item.type) && item.visible !== false" :label="item.label">
                    <el-button :class="{ disabledbtn: item.disabled }" @click.stop="handTable(item)">
                        <el-icon :size="20"><Grid /></el-icon>
                    </el-button> 
                </el-form-item>
            </template>
            <div v-else style="height: 100px;">暂无数据</div>
        </el-form>
    </div>
</template>

<script>
import { rootStore } from '@/stores/rootStore';
import { getComputedGet, getComputedSet, isEmpty} from '@/utils/utils';
import { useEventCentre } from '@/hooks/useEventCentre';

const { onClickOther, onChange } = useEventCentre();
export default {
    props: {
        propValue: {
            type: Object,
            default: () => ({
                activateText: "",
                size: 'small',
                labelPosition: 'right',
                formData: [
                    {
                        name: 'ErFormItem1',
                        label: '表单项1',
                        visible: true,
                        type: 'input',
                        value: '',
                    },
                    {
                        name: 'ErFormItem2',
                        label: '表单项2',
                        visible: true,
                        type: 'input',
                        value: '',
                    },
                ],
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    methods: {
        isEmpty,
        handleValueChange(newVal, item) {
            onChange({element: this.element, newValue: newVal, oldValue: this.oldValue, params: { item, activateText: this.activateText}})
        },
        handTable(item) {
            onClickOther({element: this.element, clickName: 'onTable', params: { item, activateText: this.activateText}})
        },
    },
    computed: {
        size: {
            get() {
                return getComputedGet('size', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('size', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        labelPosition: {
            get() {
                return getComputedGet('labelPosition', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('labelPosition', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
            }
        },
        formData: {
            get() {
                return getComputedGet('formData', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue)
            },
            set(val) {
                getComputedSet('formData', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue, val)
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
    },
}
</script>

<style lang="less" scoped>
.disabledbtn {
    cursor: not-allowed;
    pointer-events: none;
    opacity: 0.5;
}
</style>
