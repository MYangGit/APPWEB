
<script setup>
import DataSet from './DataSet.vue';
import ActionJsSet from './ActionJsSet.vue';
import ActionJuliaSet from './ActionJuliaSet.vue';
import ActionPythonSet from './ActionPythonSet.vue';
import StateWatch from './StateWatch.vue';
import LanguageSwitch from './module/LanguageSwitch.vue';
import { useProgramLanguage } from '@/hooks/useProgramLanguage';
import { ref } from 'vue';
const Language = useProgramLanguage();
const activeName = ref('state');
</script>
<template>
  <div class="data-center-panel">
    <el-tabs v-model="activeName">
      <el-tab-pane name="state" label="数据">
        <DataSet/>
      </el-tab-pane>
      <el-tab-pane name="action" label="动作">
        <ActionJsSet v-if="Language.cunLanguage === 'Javascript'"/>
        <ActionJuliaSet v-if="Language.cunLanguage === 'Julia'"/>
        <ActionPythonSet v-if="Language.cunLanguage === 'Python'"/>
      </el-tab-pane>
      <el-tab-pane name="stateWatch" label="数据监听">
        <StateWatch/>
      </el-tab-pane>
    </el-tabs>
    <div class="language-switch">
      <LanguageSwitch />
    </div>
  </div>
</template>
<style lang="less" scoped>
.data-center-panel {
  position: relative;
  height: 100%;
  background-color: #ffffff;
  padding: 0 10px;
}
.language-switch {
  position: absolute;
  top: 14px;
  right: 10px;
}
</style>
