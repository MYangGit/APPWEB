<template>
    <div @mouseenter="onMouseEnter">
        <component
            :is="config.component"
            ref="component"
            class="component"
            @click="handleActionClick"
            v-if="getShowState(config)"
            :style="getStyle(config.style)"
            :prop-value="config.propValue"
            :element="config"
            :linkage="config.linkage"
        />
    </div>
</template>

<script>
import { getStyle } from '@/utils/style';
import runAnimation from '@/utils/runAnimation';
import { mixins } from '@/utils/events';
import eventBus from '@/utils/eventBus';
import { getValueByDotKey } from '@/utils/utils'
import { rootStore } from '@/stores/rootStore';
import { useEventCentre } from '@/hooks/useEventCentre';

const { onClick } = useEventCentre();
export default {
    mixins: [mixins],
    props: {
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
            console.log(config.visiable)
            if (!config.visiable.key) return true
            let value = getValueByDotKey(rootStore.dataConfig.stateSet, config.visiable.key.join('.'))
            return value === config.visiable.value
        },
        handleActionClick () {
            onClick({element: this.config})
        },

        onMouseEnter() {
            const linkageEvents = this.config.linkage.data.filter((i) => i.event === 'v-hover');
            if (linkageEvents.length) {
                eventBus.$emit('v-hover', linkageEvents);
            }
        },
        childMounted() {
            console.log(1111, this.$refs.component)
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
