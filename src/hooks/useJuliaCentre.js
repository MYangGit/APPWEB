import { rootStore } from '@/stores/rootStore';
import { defineStore } from 'pinia'
import { ref, watch } from 'vue';
import { isEmpty, nameRepeat } from '@/utils/utils';


/**
 * @description 支持Julia代码编程语言控制中心
 * @returns 
 */
export const useJuliaCentre = defineStore('useJulia', () => {
    // Julia函数列表
    const juliaFunList = ref([]);
    // 设置Julia函数列表
    const setJuliaFunList = ({type, uuidName, data}) => {
        const operations = {
            clear: () => juliaFunList.value = [],
            add: () => {
                if (isEmpty(uuidName)) return;
                const name = nameRepeat(uuidName, juliaFunList.value);
                juliaFunList.value = [...juliaFunList.value, {...data, name}]
                setCurrentFun(name);
            },
            delete: () => {
                if (isEmpty(uuidName)) return;
                const newjuliaFunList = juliaFunList.value?.filter(item => item.name !== uuidName);
                if(isEmpty(newjuliaFunList)) {
                    clearAllJulia()
                    return;
                }
                juliaFunList.value = [...newjuliaFunList];
                setCurrentFun(newjuliaFunList[0].name)
            },
            default: () => {
                if (isEmpty(uuidName) && isEmpty(data)) return;
                const newjuliaFunList = juliaFunList.value?.map(item => (item.name === uuidName ? { ...item, ...data } : item));
                juliaFunList.value = [...newjuliaFunList];
            },
        };
        const operation = operations[type] || operations.default;
        operation();
    }
    // 当前函数
    const currentFun = ref({});
    const setCurrentFun = (name) => {
        if(isEmpty(name)) return;
        const currentFunData = juliaFunList.value.find(item => item.name === name);
        if(isEmpty(currentFunData)) return;
        currentFun.value = currentFunData;
    }
    // 更新局部 局部再更新全局
    const updateCurrentFunProps = ({type, data}) => {
        if(isEmpty(data) && isEmpty(currentFun.value)) return;
        if(type === 'delete') {
            const newProps = Object.keys(currentFun.value.props).reduce((acc, key) => {
                if(!data[key]) {
                    acc[key] = currentFun.value.props[key];
                }
                return acc;
            }, {});
            currentFun.value.props = newProps;
            setJuliaFunList({uuidName: currentFun.value.name, data: currentFun.value})
            return;
        }
        currentFun.value.props = {...currentFun.value.props, ...data};
        setJuliaFunList({uuidName: currentFun.value.name, data: currentFun.value})
    }
    // 清空所有函数
    const clearAllJulia = () => {
        juliaFunList.value = [];
        currentFun.value = {};
    }

    const init_juliaFun = (nameFlag) => {
        const juliaFun = Object.keys(rootStore.dataConfig.actionSet).reduce((acc, key) => {
            if(key.includes(nameFlag)) {
                acc.push(JSON.parse(rootStore.dataConfig.actionSet[key]))
            }
            return acc;
        }, [])
        if(isEmpty(juliaFun)) return;
        juliaFunList.value = juliaFun;
    }
    // 初始化区域
    const init = () => {
        if(!isEmpty(juliaFunList.value)){
            setCurrentFun(juliaFunList.value[0].name);
        };
        init_juliaFun("Julia@");
    }
    init();

    const handleDelete = (name) => {
        delete rootStore.dataConfig.actionSet[name]
    }
    watch(currentFun, (newVal, oldVal) => {
        if(isEmpty(newVal) && !isEmpty(oldVal))  {
            handleDelete(`${oldVal.type}@${oldVal.name}`)
            return;
        };
        rootStore.dataConfig.addAction(`${newVal.type}@${newVal.name}`, JSON.stringify(newVal))
    })
    
    return {
        juliaFunList,
        currentFun,
        setJuliaFunList,
        setCurrentFun,
        updateCurrentFunProps
    }
});