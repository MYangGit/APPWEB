import { 
  post, 
  postMessage, 
  getFilePath, 
  initFilePath, 
  checkValHas,
  importDesignFile,
  exportDesignFile,
  closeApp,
  generateReport,
  commonImportFile
} from '@/services/request/connectBase'
import { handleJuliaCode } from '@/hooks/useJuliaCentre'
import { handlePythonCode } from '@/hooks/usePythonCentre'
import { rootStore } from '@/stores/rootStore'
import { isEmpty, nameRepeat, createUuid, getObjValue, deepCopy } from '@/utils/utils'
import { returnData } from '@/constant'

/**
 * @description 全局公共方法暴露中心
 * @returns 
*/
export const useGlobalUtils = () => {
  return {
    returnData,
    getObjValue,
    createUuid,
    deepCopy,
    commonImportFile,
    getObjValue,
    generateReport,
    createUuid,
    closeApp,
    importDesignFile,
    exportDesignFile,
    commonImportFile,
    post,
    postMessage,
    getFilePath,
    initFilePath,
    checkValHas,
    openConfirmBox: rootStore.confirmBox.openConfirmBox,
    handleJuliaCode,
    handlePythonCode,
    isEmpty,
    nameRepeat
  }
}