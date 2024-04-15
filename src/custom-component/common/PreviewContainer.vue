<template>
    <div 
        :id="name" 
        class="content"
        :style="getFlexStyle()"
    >
        <ComponentWrapper :layoutType="layoutType" v-for="(item, index) in childs" :key="index" :config="item" />
    </div>
</template>

<script>
import ComponentWrapper from '../../components/Editor/ComponentWrapper';

export default {
    name: 'PreviewContainer',
    components: {
        ComponentWrapper,
    },
    props: {
        layoutType: {
            type: String,
            default: 'normal',
        },
        flexOptions: {
            type: Object,
            default: () => {}
        },
        propValue: {
            type: Array,
            default: () => [],
        },
        element: {
            type: Object,
            default: () => {},
        },
        name: {
            type: String,
            default: () => '1',
        },
        childs: {
            type: Array,
            default: () => [],
        },
    },
    data() {
        return {};
    },
    methods: {
        getFlexStyle () {
            if(!this.flexOptions) return {}
            let { direction, horAlign, verAlign, wrapType} = this.flexOptions;
            let styles = {}
            styles.display = 'flex';
            styles['flex-direction'] = direction
            styles['justify-content'] = horAlign
            styles['align-items'] = verAlign
            styles['flex-wrap'] = wrapType
            return styles
        }
    },
};
</script>

<style lang="less" scoped>
.content {
    width: 100%;
    height: 100%;
    overflow: auto;
    position: relative;
}
.active {
    border: 1px solid #70c0ff;
    user-select: none;
    box-sizing: content-box;
}
</style>
