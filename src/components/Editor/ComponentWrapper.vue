<template>
    <div @mouseenter="onMouseEnter">
        <component
            :is="config.component"
            ref="component"
            :class="layoutType === 'flex' ? 'flex-component' : 'component'"
            @click="handleActionClick"
            v-if="getShowState(config)"
            :style="getStyle(config.style)"
            :prop-value="config.propValue"
            :element="config"
        />
    </div>
</template>

<script>
import { getStyle } from '@/utils/style';
import runAnimation from '@/utils/runAnimation';
import { mixins } from '@/utils/events';
import { getValueByDotKey } from '@/utils/utils'
import { rootStore } from '@/stores/rootStore';
import { useEventCentre } from '@/hooks/useEventCentre';
import { isEmpty } from '@/utils/utils';

const { onClick } = useEventCentre();
export default {
    mixins: [mixins],
    props: {
        layoutType: {
            type: String,
            default: 'normal',
        },
        config: {
            type: Object,
            required: true,
            default: () => {},
        },
    },
    mounted() {
        this.childMounted()
    },
    methods: {
        getStyle,
        getShowState (config) {
            if (!config.visiable) return true
            if (!config.visiable.key) return true
            let value = getValueByDotKey(rootStore.dataConfig.stateSet, config.visiable.key.join('.'))
            if(isEmpty(config.visiable.value)) {
                return value
            }
            // 如果第一个字符是！，则取反
            if (config.visiable.value.startsWith('!')) {
                return value !== config.visiable.value.slice(1)
            }
            return value === config.visiable.value
        },
        handleActionClick () {
            onClick({element: this.config})
        },
        childMounted() {
            if (this.$refs.component) {
                runAnimation(this.$refs.component.$el, this.config.animations);
            }
        },
    },
};
</script>

<style lang="less" scoped>
.component {
    position: absolute;
}
</style>
