<template>
    <div class="input-wrap">
        <label v-show="propValue.label">{{ propValue.label }}：</label>
        <el-input-number v-model="propValue.value" :precision="propValue.precision" :step="propValue.step" :max="propValue.max" :min="propValue.min"></el-input-number>
    </div>
</template>

<script>
import eventBus from '@/utils/eventBus';
import OnEvent from '../common/OnEvent'

export default {
    extends: OnEvent,
    props: {
        propValue: {
            type: Object,
            default: () => ({
                label: '',
                key: '',
                value: '',
                precision: 0,
                step: 1,
                max: 100,
                min: 0,
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
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
