<template>
    <div>
        <erStatusBar style="width: 100%;height: 100%;" :message="message">
            <erRollLoading :loading="isLoading"/>
        </erStatusBar>
    </div>
</template>

<script>
import OnEvent from '../../common/OnEvent'
import { getComputedGet } from '../../../utils/utils'
import { rootStore } from '@/stores/rootStore';

export default {
    extends: OnEvent,
    props: {
        propValue: {
            type: Object,
            default: () => ({
                message: '',
                isLoading: false,
            }),
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    computed: {
        message: {
            get () {
                return getComputedGet('message', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue) || ''
            }
        },
        isLoading: {
            get () {
                return getComputedGet('isLoading', this.element.dataBinds, rootStore.dataConfig.stateSet, this.propValue) || false
            }
        },
    },
    mounted() {
    }
}
</script>

<style lang="less" scoped>
</style>
