<template>
    <div class="exercise">
        <!-- <codemirror v-model="code" :options="cmOptions" /> -->
        <codemirror
            v-model="code"
            :style="{ height: '400px' }"
            :autofocus="true"
            :indent-with-tab="true"
            :tab-size="2"
            :extensions="extensions"
        />
    </div>
</template>
<script setup>
import { Codemirror } from 'vue-codemirror'
import { useDataCenterStore } from '@/stores/dataCenter'
import { computed } from 'vue';

const dataCenterStore = useDataCenterStore()
const extensions = []
const code = computed({
    get() {
        return JSON.stringify(dataCenterStore.componentData.value, null, '\t')
    },
    set(newValue) {
        dataCenterStore.setComponentData(JSON.parse(newValue || '[]'))
    }
})
</script>
<style>
/* 注意：这里的样式需要全局，如果写了scoped会导致样式不生效 */
.CodeMirror {
    border: 1px solid #eee;
    height: 100%; /* 编辑器盒子高度自适应 */
    width: 100%;
}
.exercise,
.cm-editor {
    height: 100%;
}
</style>
