import { ref } from 'vue'
import { defineStore } from 'pinia'
import defer from 'defer-promise'

let deferred = defer();

export const useConfirmBoxStore = defineStore('confirmBox', () => {
  const confirmBoxState = ref({
    isShow: false,
    title: '',
    message: '',
    sureText: '',
    cancelText: '',
    width: 400,
    height: 50,
  });
  const openConfirmBox = async (options) => {
    deferred = defer();
    confirmBoxState.value = {
      ...confirmBoxState.value,
      ...options,
      isShow: true
    }
    await deferred.promise;
  }
  const rejectConfirmBox = () => {
    confirmBoxState.value.isShow = false
    confirmBoxState.value.height = 50;
    confirmBoxState.value.width = 400;
    deferred.reject();
  }
  const resolveConfirmBox = () => {
    confirmBoxState.value.isShow = false
    confirmBoxState.value.height = 50;
    confirmBoxState.value.width = 400;
    deferred.resolve();
  }
  return {
    confirmBoxState,
    openConfirmBox,
    rejectConfirmBox,
    resolveConfirmBox
  }
})
