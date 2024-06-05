<template>
    <div>
        <component :is="autoTemplate" />
    </div> 
</template>

<script setup>
import { isEmpty } from '@/utils/utils';
import { watch, ref } from 'vue';

const props = defineProps(
    {
        propValue: {
            type: Object,
            default: () => ({
                codingName: '',
            }),
        },
        element: {
            type: Object,
            default: () => {},
        }
    }
);
let autoTemplate = ref(null);
watch(() => props.propValue.codingName, (newVal) => {
    if(isEmpty(newVal)) return;
    autoTemplate.value = newVal;
});
</script>
