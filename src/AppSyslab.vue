<template>
  <Preview />
</template>

<script setup>
  import Preview from '@/components/Editor/Preview.vue'
  import AppInfo from '../packages/syslab/syslabApp.json';
  import WebInfo from '../packages/web/syslabApp.json';
  import { rootStore } from '@/stores/rootStore';
  import { isSyslabApp } from '@/utils/isPreviewOrApp'
  const init = () => {
    const data = isSyslabApp() ? AppInfo : WebInfo;
    rootStore.dataConfig.stateSet = data.dataCenter
    rootStore.dataConfig.actionSet = data.actionCenter
    rootStore.dataConfig.watchRegisters = data.watchRegisters
    rootStore.dataCenter.setComponentData(data.components)
  }
  init()
</script>
<style>
button:focus {
  outline: none !important;
}
</style>

<style>
button:focus {
  outline: none !important;
}
</style>

 
