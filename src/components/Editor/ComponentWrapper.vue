<template>
    <div @mouseenter="onMouseEnter">
        <div v-if="isShow">
            <component
                :is="config.component"
                v-show="getShowState(config)"
                ref="component"
                :class="layoutType === 'flex' ? 'flex-component' : 'component'"
                @click="handleActionClick"
                :style="getStyle(config.style)"
                :prop-value="config.propValue"
                :element="config"
            />
      </div>
      <div v-else>
            <component
                :is="config.component"
                v-if="getShowState(config)"
                ref="component"
                :class="layoutType === 'flex' ? 'flex-component' : 'component'"
                @click="handleActionClick"
                :style="getStyle(config.style)"
                :prop-value="config.propValue"
                :element="config"
            />
      </div>
    </div>
</template>

<script>
import { getStyle } from '@/utils/style';
import runAnimation from '@/utils/runAnimation';
import { mixins } from '@/utils/events';
import { getValueByDotKey, isEmpty } from '@/utils/utils'
import { rootStore } from '@/stores/rootStore';
import { useEventCentre } from '@/hooks/useEventCentre';

const { onClick } = useEventCentre();
export default {
    mixins: [mixins],
    props: {
        layoutType: {
            type: String,
            default: 'normal',
        },
        isShow: {
            type: Boolean,
            default: false,
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
                let userValues = config.visiable.value.slice(1)
                if (userValues.includes(',')) {
                    return !userValues.split(',').includes(value)
                }
                return value !== userValues
            }
            // 如果是,则是多个值
            if (config.visiable.value.includes(',')) {
                return config.visiable.value.split(',').includes(value)
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
