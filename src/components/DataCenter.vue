
<script setup>
import DataSet from './DataSet.vue';
import ActionSet from './ActionSet.vue';
import StateWatch from './StateWatch.vue';
import { ref } from 'vue';

const activeName = ref('state');

</script>
<template>
  <div class="data-center-panel">
    <el-tabs v-model="activeName">
      <el-tab-pane name="state" label="数据">
        <DataSet></DataSet>
      </el-tab-pane>
      <el-tab-pane name="action" label="动作">
        <ActionSet></ActionSet>
      </el-tab-pane>
      <el-tab-pane name="stateWatch" label="数据监听">
        <StateWatch></StateWatch>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
<style lang="less" scoped>
.data-center-panel {
  height: 100%;
  background-color: #ffffff;
  padding: 0 10px;
}
</style>
