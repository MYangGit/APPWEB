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
import { handleJuliaCode } from '@/hooks/useJuliaCentre'
import { rootStore } from '@/stores/rootStore'

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
    checkValHas,
    openConfirmBox: rootStore.confirmBox.openConfirmBox,
    handleJuliaCode
  }
}