<template>
    <div @click="onClick" @mouseenter="onMouseEnter">
        <component
            :is="config.component"
            v-if="config.component.startsWith('SVG')"
            ref="component"
            class="component"
            :style="getSVGStyle(config.style)"
            :prop-value="config.propValue"
            :element="config"
            :request="config.request"
            :linkage="config.linkage"
            @hook:mounted="childMounted"
        />

        <component
            :is="config.component"
            v-else
            ref="component"
            class="component"
            :style="getStyle(config.style)"
            :prop-value="config.propValue"
            :element="config"
            :request="config.request"
            :linkage="config.linkage"
            @hook:mounted="childMounted"
        />
    </div>
</template>

<script>
import { getStyle, getSVGStyle } from '@/utils/style';
import runAnimation from '@/utils/runAnimation';
import { mixins } from '@/utils/events';
import eventBus from '@/utils/eventBus';

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
        // 对于懒加载的组件不生效
        // if (this.$refs.component) {
        //     runAnimation(this.$refs.component.$el, this.config.animations);
        // }
    },
    methods: {
        getStyle,
        getSVGStyle,

        onClick() {
            const events = this.config.events;
            Object.keys(events).forEach((event) => {
                this[event](events[event]);
            });
            const linkageEvents = this.config.linkage.data.filter((i) => i.event === 'v-click');
            if (linkageEvents.length) {
                eventBus.$emit('v-click', linkageEvents);
            }
        },

        onMouseEnter() {
            const linkageEvents = this.config.linkage.data.filter((i) => i.event === 'v-hover');
            if (linkageEvents.length) {
                eventBus.$emit('v-hover', linkageEvents);
            }
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
