
<script setup>
import { computed, ref } from 'vue'
import { Codemirror } from 'vue-codemirror'
import { noctisLilac } from 'thememirror'
import { json } from "@codemirror/lang-json"
import { rootStore } from '@/stores/rootStore'

const extensions = [json(), noctisLilac]

const editor = ref()

const code = computed({
  get() {
    return JSON.stringify(rootStore.dataConfig.stateSet, null, '\t')
  },
  set(value) {
    let state = ''
    try {
      state = JSON.parse(value)
    } catch (error) {
      console.error('json格式异常，当前变更无法同步')
    }
    if (state) {
      rootStore.dataConfig.stateSet = state
      console.log('已同步')
    }
  }
})

</script>

<template>
  <div class="data-set-wrapper">
    <codemirror
      ref="editor"
      v-model="code"
      :autofocus="false"
      :indent-with-tab="true"
      :tab-size="2"
      :extensions="extensions"
    />
  </div>
</template>
<style lang="less" scoped>
.data-set-wrapper {
  height: 100%;
}
</style>
