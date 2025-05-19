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

    // 表格数组转换为值数组
    function transformToValueArray(columns, dataSource, formatter = (val) => val) {
        if(!Array.isArray(columns) || !Array.isArray(dataSource)) {
            return [];
        }
        const keys = columns.map(col => col.key);
        return dataSource.map(item => 
            keys.map(key => formatter(item[key], key))
        );
    }
    
    return {
        disablePro,
        transformToValueArray,
    }
}