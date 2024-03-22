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
        />

        <component
            :is="config.component"
            v-else
            ref="component"
            class="component"
            @click="handleActionClick"
            :style="getStyle(config.style)"
            :prop-value="config.propValue"
            :element="config"
            :linkage="config.linkage"
        />
    </div>
</template>

<script>
import { getStyle, getSVGStyle } from '@/utils/style';
import runAnimation from '@/utils/runAnimation';
import { mixins } from '@/utils/events';
import eventBus from '@/utils/eventBus';
import { rootStore } from '@/stores/rootStore';

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
        getSVGStyle,
        handleActionClick () {
            let { click } = this.config.actionBinds;
            if (!click) return
            let fn = new Function(`return ${rootStore.dataConfig.actionSet[click]}`)()
            fn(rootStore.dataConfig.stateSet, {
                post: (data) => {
                    console.log('post', data)
                }
            })
        },
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
