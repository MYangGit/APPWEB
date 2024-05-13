
import { ref, watch } from 'vue'
import { defineStore } from 'pinia'
import localforage from 'localforage';
import isPreviewOrApp from '@/utils/isPreviewOrApp';

export const useDataConfigStore = defineStore('dataConfig', () => {
  const stateSet = ref({})
  const actionSet = ref({})
  const watchRegisters = ref([])

  localforage.getItem('stateSet').then(cp => {
    if (!cp) return
    if (Object.keys(stateSet.value).length === 0) stateSet.value = JSON.parse(cp)
  })

  watch(stateSet, () => {
    if (isPreviewOrApp()) return
    localforage.setItem('stateSet', JSON.stringify(stateSet.value))
  }, {
    deep: true
  })

  localforage.getItem('actionSet').then(cp => {
    if (!cp) return
    if (Object.keys(actionSet.value).length === 0) actionSet.value = JSON.parse(cp)
  })

  watch(actionSet, () => {
    if (isPreviewOrApp()) return
    localforage.setItem('actionSet', JSON.stringify(actionSet.value))
  }, {
    deep: true
  })

  localforage.getItem('watchRegisters').then(cp => {
    if (!cp) return
    if (watchRegisters.value.length === 0) watchRegisters.value = JSON.parse(cp)
  })

  watch(watchRegisters, () => {
    if (isPreviewOrApp()) return
    localforage.setItem('watchRegisters', JSON.stringify(watchRegisters.value))
  }, {
    deep: true
  })

  const addState = (key, value) => {
    stateSet.value[key] = value
  }
  const deleteState = (key) => {
    delete stateSet.value[key]
  }

  const addAction = (key, value) => {
    actionSet.value[key] = value
  }
  const deleteAction = (key) => {
    delete actionSet.value[key]
  }
  return {
    stateSet,
    actionSet,
    watchRegisters,
    addState,
    deleteState,
    addAction,
    deleteAction
  }
})
