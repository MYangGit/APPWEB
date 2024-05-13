
import { ref, watch } from 'vue'
import { defineStore } from 'pinia'
import localforage from 'localforage';

export const useDataConfigStore = defineStore('dataConfig', () => {
  const stateSet = ref({})
  const actionSet = ref({})
  const watchRegisters = ref([])

  if (import.meta.env.VITE_NODE_ENV !== 'SyslabApp') {
    localforage.getItem('stateSet').then(cp => {
      if (!cp) return
      stateSet.value = JSON.parse(cp)
    })
  
    watch(stateSet, () => {
      localforage.setItem('stateSet', JSON.stringify(stateSet.value))
    }, {
      deep: true
    })
  
    localforage.getItem('actionSet').then(cp => {
      if (!cp) return
      actionSet.value = JSON.parse(cp)
    })
  
    watch(actionSet, () => {
      localforage.setItem('actionSet', JSON.stringify(actionSet.value))
    }, {
      deep: true
    })
  
    localforage.getItem('watchRegisters').then(cp => {
      if (!cp) return
      watchRegisters.value = JSON.parse(cp)
    })
  
    watch(watchRegisters, () => {
      localforage.setItem('watchRegisters', JSON.stringify(watchRegisters.value))
    }, {
      deep: true
    })
  }
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
