
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useDataConfigStore = defineStore('dataConfig', () => {
  const stateSet = ref({
    form: {
      name: 'Tom',
      age: 10,
      cat: {
        name: 'TomCat',
        age: 10
      },
      dog: {
        name: 'TomDog',
        age: 10
      }
    },
    tip: 'hello world'
  })
  const actionSet = ref({
    submit: `(dataCenter, globalUtils) => {
  //Todo
}`
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
    addState,
    deleteState,
    addAction,
    deleteAction
  }
})
