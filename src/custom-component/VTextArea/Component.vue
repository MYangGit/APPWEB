<template>
    <div class="input-wrap">
        <label v-show="propValue.label">{{ propValue.label }}：</label>
        <el-input v-model="propValue.value" size="small" type="textarea" />
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
    align-items: baseline;
    label {
        word-break: keep-all;
        white-space: nowrap;
    }
}
</style>
