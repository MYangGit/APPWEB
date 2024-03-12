<template>
    <div class="attr-list">
        <CommonAttr>
        </CommonAttr>
    </div>
</template>

<script>
import CommonAttr from '@/custom-component/common/CommonAttr.vue'
import { rootStore } from '@/stores/rootStore';

export default {
    components: { CommonAttr },
    computed: {
        propValue() {
            return rootStore.dataCenter.curComponent.propValue;
        },
    },
};
</script>
