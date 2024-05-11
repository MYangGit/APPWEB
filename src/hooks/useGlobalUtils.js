import { 
  post, 
  postMessage, 
  getFilePath, 
  initFilePath, 
  checkValHas,
  importDesignFile,
  exportDesignFile
} from '@/services/request/connectBase'
import { returnData } from '@/constant'
/**
 * @description 全局公共方法暴露中心
 * @returns 
*/
export const useGlobalUtils = () => {
  return {
    returnData,
    importDesignFile,
    exportDesignFile,
    post,
    postMessage,
    getFilePath,
    initFilePath,
    checkValHas
  }
}