
<script setup>
import { computed, ref } from 'vue'
import { Codemirror } from 'vue-codemirror'
import { noctisLilac } from 'thememirror'
import { json } from "@codemirror/lang-json"
import { rootStore } from '@/stores/rootStore'

const extensions = [json(), noctisLilac]

const hasError = ref(false)

const editor = ref()

const tmpState = ref(rootStore.dataConfig.stateSet)

const code = computed({
  get() {
    return JSON.stringify(rootStore.dataConfig.stateSet, null, '\t')
  },
  set(value) {
    let state = ''
    try {
      state = JSON.parse(value)
      hasError.value = false
    } catch (error) {
      hasError.value = true
    }
    if (!hasError.value) {
      tmpState.value = state
    }
  }
})

const handleBlur = () => {
  rootStore.dataConfig.stateSet = tmpState.value
}

</script>

<template>
  <div class="data-set-wrapper">
    <codemirror
      ref="editor"
      v-model="code"
      :autofocus="false"
      @blur="handleBlur"
      :indent-with-tab="true"
      :tab-size="2"
      :extensions="extensions"
    />
    <div class="status-bar" :class="hasError ? 'red': 'green' ">{{ hasError ? '数据格式错误' : '正常' }}</div>
  </div>
</template>
<style lang="less" scoped>
.data-set-wrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.status-bar {
  display: flex;
  align-items: center;
  font-size: 12px;
  padding: 3px 0 3px 10px;
  &.green {
    color: #ffffff;
    background-color: #67C23A;
  }
  &.red {
    color: #ffffff;
    background-color: #F56C6C;
  }
}
</style>
