
<script setup>
import DataSet from './DataSet.vue';
import ActionJsSet from './ActionJsSet.vue';
import ActionJuliaSet from './ActionJuliaSet.vue';
import ActionPythonSet from './ActionPythonSet.vue';
import StateWatch from './StateWatch.vue';
import { ref } from 'vue';
import { useProgramLanguage } from '@/hooks/useProgramLanguage';
const { cunLanguage, setCunLanguage } = useProgramLanguage();
const activeName = ref('state');
const useLanguage = ref(cunLanguage);
const handleCommand = (command) => {
  setCunLanguage(command);
  useLanguage.value = command;
};

</script>
<template>
  <div class="data-center-panel">
    <el-tabs v-model="activeName">
      <el-tab-pane name="state" label="数据">
        <DataSet/>
      </el-tab-pane>
      <el-tab-pane name="action" label="动作">
        <ActionJsSet v-if="useLanguage === 'Javascript'"/>
        <ActionJuliaSet v-if="useLanguage === 'Julia'"/>
        <ActionPythonSet v-if="useLanguage === 'Python'"/>
      </el-tab-pane>
      <el-tab-pane name="stateWatch" label="数据监听">
        <StateWatch/>
      </el-tab-pane>
    </el-tabs>
    <div class="language-switch">
      <el-dropdown @command="handleCommand">
        <span class="el-dropdown-link">
          编程语言：{{ useLanguage }}
          <el-icon class="el-icon--right">
            <arrow-down />
          </el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="Javascript" >Javascript</el-dropdown-item>
            <el-dropdown-item command="Julia" >Julia</el-dropdown-item>
            <el-dropdown-item command="Python">Python</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
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
.el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}
</style>
