<template>
    <div>
        <CommonAttr>
        </CommonAttr>
    </div>
</template>

<script>
import CommonAttr from '@/custom-component/common/CommonAttr.vue';
import { rootStore } from '@/stores/rootStore';
import { useCodingCentre } from '@/hooks/useCodingCentre';
const { codingComponents } = useCodingCentre();

export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
        options(){
            return codingComponents
        }
    },
};
</script>
