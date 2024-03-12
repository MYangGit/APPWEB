<script>
import eventBus from '@/utils/eventBus';
/* eslint-disable function-paren-newline */

export default {
    props: {
        linkage: {
            type: Object,
            default: () => {},
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    created() {
        if (this.linkage?.data?.length) {
            eventBus.$on('v-click', (componentData) => this.onClick(componentData, 'v-click'));
            eventBus.$on('v-hover', (componentData) => this.onClick(componentData, 'v-hover'));
            eventBus.$on('handleNodeClick', (componentData, data) =>
                this.onClick(componentData, 'handleNodeClick', data),
            );
            eventBus.$on('updateModelTab', (componentData, data) =>
                this.onClick(componentData, 'updateModelTab', data),
            );
            eventBus.$on('componentChange', (componentData, data) =>
                this.onClick(componentData, 'componentChange', data),
            );
            eventBus.$on('updateSvgViewer', (componentData, data) =>
                this.onClick(componentData, 'updateSvgViewer', data),
            );
            eventBus.$on('simulateCompleted', (componentData, data) =>
                this.onClick(componentData, 'simulateCompleted', data),
            );
            eventBus.$on('updateAxisPointer', (componentData, data) =>
                this.onClick(componentData, 'updateAxisPointer', data),
            );
            eventBus.$on('updateValue', (componentData, data) =>
                this.onClick(componentData, 'updateValue', data),
            );
        }
    },
    mounted() {
        const { data, duration } = this.linkage || {};
        if (data?.length) {
            this.$el.style.transition = `all ${duration}s`;
        }
    },
    beforeDestroy() {
        if (this.linkage?.data?.length) {
            eventBus.$off('v-click', this.onClick);
            eventBus.$off('v-hover', this.onClick);
            eventBus.$off('handleNodeClick', this.onClick);
        }
    },
    methods: {
        changeStyle(data = []) {
            data.forEach((item) => {
                item.style.forEach((e) => {
                    if (e.key) {
                        this.element.style[e.key] = e.value;
                    }
                });
            });
        },

        emitEvent(data = [], params) {
            data.forEach((item) => {
                item.events.forEach((e) => {
                    if (e.name) {
                        this[e.name](params);
                    }
                });
            });
        },

        onClick(componentData, eventType, params) {
            const componentId = componentData.map((i) => i.id);
            if (componentId.includes(this.element.id)) {
                const data = componentData.filter((item) => item.id === this.element.id && item.event === eventType);
                this.changeStyle(data);
                this.emitEvent(data, params);
            }
        },
    },
};
</script>
