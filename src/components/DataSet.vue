
<script setup>
import { ref } from 'vue'
import { Codemirror } from 'vue-codemirror'
import { noctisLilac } from 'thememirror'
import { json } from "@codemirror/lang-json"
import { rootStore } from '@/stores/rootStore'

const extensions = [json(), noctisLilac]
const activeName = ref('')

activeName.value = rootStore.dataConfig.stateList[0].name
</script>

<template>
  <el-tabs tab-position="left" v-model="activeName">
    <el-tab-pane :name="state.name" :label="state.name" v-for="state in rootStore.dataConfig.stateList" :key="state.name">
      <codemirror
        v-model="state.value"
        :autofocus="true"
        :indent-with-tab="true"
        :tab-size="2"
        :extensions="extensions"
      />
      <div class="btns-wrapper">
        <el-button type="primary">删除</el-button>
      </div>
    </el-tab-pane>
  </el-tabs>
</template>
<style lang="less" scoped>

</style>
