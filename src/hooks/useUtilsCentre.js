import { isEmpty } from '@/utils/utils';

/**
 * @description 公共方法维护中心
 * @author MY
 * @date 2025-05-08 16:00:00
 * @returns
*/
export const useUtilsCentre = () => {
    /**
     * @description 禁用 pro 版功能
     * @returns
    */
    const disablePro = (disVal, disabledText = "") => {
        if(typeof disVal === "boolean"){
            if(disabledText === "!"){
               return !disVal
            }
            return disVal
        }
        if(!isEmpty(disabledText)){
            if(disabledText.startsWith("!")){
                return disVal !== disabledText.substring(1)
            }
            return (disVal === disabledText)
        }
        return isEmpty(disVal)
    }
    
    return {
        disablePro,
    }
}