import VButton from './VButton/meta';
import VHtml from './VHtml/meta';
import VInput from './VInput/meta';
import VPlot from './VPlot/meta';
import VText from './VText/meta';
import VSelect from './VSelect/meta';
import VCheckBox from './VCheckBox/meta';
import VRadio from './VRadio/meta';
import VTextArea from './VTextArea/meta';
// 编辑器左侧组件列表
const componentList = [
    VButton,
    VHtml,
    VInput,
    VPlot,
    VText,
    VSelect,
    VCheckBox,
    VRadio,
    VTextArea
];

export const commonStyle = {
    rotate: 0,
    opacity: 1,
};

export const commonAttr = {
    animations: [],
    dataBinds: {},
    actionBinds: {},
    groupStyle: {}, // 当一个组件成为 Group 的子组件时使用
    isLock: false, // 是否锁定组件
    collapseName: '', // 编辑组件时记录当前使用的是哪个折叠面板，再次回来时恢复上次打开的折叠面板，优化用户体验
    linkage: {
        duration: 0,
        data: [
            // 组件联动
            {
                id: '',
                label: '',
                event: '',
                style: [{ key: '', value: '' }],
                events: [{ name: '' }],
            },
        ],
    }
};

// 把组件数据重新分配定义
for (let i = 0, len = componentList.length; i < len; i++) {
    const item = componentList[i];
    item.style = { ...commonStyle, ...item.style };
    componentList[i] = { ...commonAttr, ...item };
}

export default componentList;
