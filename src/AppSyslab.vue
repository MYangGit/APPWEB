<template>
  <Preview />
</template>

<script setup>
  import Preview from '@/components/Editor/Preview.vue'
  import AppInfo from '../packages/syslab/syslabApp.json';
  import { rootStore } from '@/stores/rootStore';
  const init = () => {
    const data = AppInfo;
    rootStore.dataConfig.stateSet = data.dataCenter
    rootStore.dataConfig.actionSet = data.actionCenter
    rootStore.dataConfig.watchRegisters = data.watchRegisters
    rootStore.dataCenter.setComponentData(data.components)
  }
  init()
</script>

