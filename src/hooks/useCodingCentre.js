
// import test from "@/components/test.vue"
/**
 * @description 手写代码物料统一暴露中心
 * @returns
*/
export const useCodingCentre = () => {
    
    // 自定义组件列表
    const codingComponents = [
        // {
        //     value: test,
        //     label: '好用的不的料',
        // }
    ]
    // 根据组件名获取组件
    const getComponent = (componentName) => {
        const component = codingComponents.find(item => item.label === componentName)
        return component ? component.value : null
    }
    return {
        codingComponents,
        getComponent
    }
}