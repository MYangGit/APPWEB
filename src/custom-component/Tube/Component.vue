<template>
    <div>
        <div :style="{ backgroundColor: color, height: `${element.style.height}px` }"></div>
        <div :style="{ color: propValue.titleColor, fontSize: `${propValue.titleSize}px`, textAlign: propValue.titleAlign }">{{ propValue.title }}</div>
    </div>
</template>

<script>
import OnEvent from '../common/OnEvent'

export default {
    extends: OnEvent,
    props: {
        propValue: {
            type: Object,
            default: () => {},
        },
        request: {
            type: Object,
            default: () => {},
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    data() {
        return {
            color: '',
        }
    },
    methods: {
        updateData(params) {
            // eslint-disable-next-line arrow-body-style
            const data = params
                .filter((i) => this.request.data.includes(i.name))
                .map((i) => ({
                    ...i,
                    value: parseFloat(i.value).toFixed(this.propValue.floatUnit),
                }));
            this.color = data[0]?.value > this.propValue.warningValue ? this.propValue.warningColor : '';
        },
        hightlight(params) {
            this.color = params === this.propValue.title ? this.propValue.warningColor : '';
        },
    },
}
</script>

<style lang="less" scoped>
</style>
