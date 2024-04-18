import { defineStore } from 'pinia'
import { ref } from 'vue';
import { isEmpty } from '@/utils/utils';

/**
 * @description 支持Julia代码编程语言控制中心
 * @returns 
 */
export const useProgramLanguage = defineStore('ProgramLanguage', () => {
    const cunLanguage = ref('Javascript');
    // 修改编程语言
    const setCunLanguage = (language) => {
        if(isEmpty(language)) return;
        cunLanguage.value = language;
    }
    const activeCunName = ref('');

    return {
        activeCunName,
        cunLanguage,
        setCunLanguage
    }
});