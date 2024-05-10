import { post, postMessage, getFilePath, initFilePath } from '@/services/request/connectBase'

/**
 * @description 全局公共方法暴露中心
 * @returns 
*/
export const useGlobalUtils = () => {
  return {
    post,
    postMessage,
    getFilePath,
    initFilePath
  }
}