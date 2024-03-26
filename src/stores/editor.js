import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useEditorStore = defineStore('editor', () => {
  const isInEdiotr = ref(false)
  const isClickComponent = ref(false)
  const editMode = ref('edit')
  const setClickComponentStatus = (status) => {
    isClickComponent.value = status;
  }
  const setInEditorStatus = (status) => {
    isInEdiotr.value = status;
  }
  const setEditMode = (mode) => {
    editMode.value = mode;
  }
  return {
    editMode,
    isInEdiotr,
    isClickComponent,
    setClickComponentStatus,
    setInEditorStatus,
    setEditMode
  }
})
