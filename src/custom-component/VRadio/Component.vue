<template>
    <div class="input-wrap">
        <label v-show="propValue.label">{{ propValue.label }}：</label>
        <el-radio-group v-if="propValue.isBtn" v-model="propValue.value">
            <el-radio-button
                v-for="item, index in propValue.options"
                :key="index"
                :value="item.value"
            >
                {{ item.label }}
            </el-radio-button>
        </el-radio-group>
        <el-radio-group v-if="!propValue.isBtn" v-model="propValue.value">
            <el-radio 
                v-for="item, index in propValue.options"
                :key="index"
                :value="item.value"
            >
                {{ item.label }}
            </el-radio>
        </el-radio-group>
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
                key: '',
                value: '',
                options: [],
                isBtn: false,
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

</style>
