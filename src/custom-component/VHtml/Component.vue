<template>
    <div ref="htmlhost" class="v-html"></div>
</template>

<script>
import OnEvent from '../common/OnEvent'

export default {
    extends: OnEvent,
    props: {
        propValue: {
            type: String,
            default: '',
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    data() {
        return {
            shadow: null,
        }
    },
    watch: {
        propValue: {
            handler(val) {
                this.shadow.innerHTML = val;
            },
        },
    },
    mounted() {
        this.shadow = this.$refs.htmlhost.attachShadow({ mode: 'open' });
        if (this.propValue) {
            this.shadow.innerHTML = this.propValue;
        }
    },
}
</script>

<style lang="less" scoped>
.v-html {
    border: 1px solid transparent;
    overflow: auto;
}
</style>
