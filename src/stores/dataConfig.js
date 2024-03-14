
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useDataConfigStore = defineStore('dataConfig', () => {
  const stateList = ref([
    {
      name: 'form',
      value: JSON.stringify({
      name: 'Tom',
      age: 10
      }, null, '\t'),
      type: 'object'
    },
    {
      name: 'tip',
      value: 'hello world',
      type: 'string'
    }
  ])
  const actionList = ref([])

  const addState = (state) => {
    stateList.value.push(state)
  }
  const deleteState = (index) => {
    stateList.value.splice(index, 1)
  }
  return {
    stateList,
    actionList,
    addState,
    deleteState
  }
})
