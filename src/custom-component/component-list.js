import VButton from './VButton/meta';
import VHtml from './VHtml/meta';
import VInput from './VInput/meta';
import VInputNumber from './VInputNumber/meta';
import VPlot from './VPlot/meta';
import VText from './VText/meta';
import VSelect from './VSelect/meta';
import VCheckBox from './VCheckBox/meta';
import VRadio from './VRadio/meta';
import VTextArea from './VTextArea/meta';
import VPanel from './VPanel/meta';
import VFlexPanel from './VFlexPanel/meta';
import VTabs from './VTabs/meta';
import ErPlot from './errantia/Plot/meta';
import ErTable from './errantia/Table/meta';
import ErInput from './errantia/Input/meta';
import ErStatusBar from './errantia/StatusBar/meta';
import ErLayout from './errantia/Layout/meta';
import ErCollapse from './errantia/Collapse/meta';
import ErDropDown from './errantia/DropDown/meta';
import ErDialog from './errantia/Dialog/meta';
import ErGrid from './errantia/Grid/meta';
import ErCheckBox from './errantia/Checkbox/meta';


// 编辑器左侧组件列表
const componentList = [
    VButton,
    VHtml,
    VInput,
    VInputNumber,
    VPlot,
    VText,
    VSelect,
    VCheckBox,
    VRadio,
    VTextArea,
    ErTable,
    ErInput,
    VPanel,
    VFlexPanel,
    VTabs,
    ErPlot,
    ErStatusBar,
    ErLayout,
    ErCollapse,
    ErDropDown,
    ErDialog,
    ErGrid,
    ErCheckBox
];

export const commonStyle = {
    rotate: 0,
    opacity: 1,
};

export const commonAttr = {
    visiable: {
        key: '',
        value: ''
    },
    animations: [],
    dataBinds: {},
    actionBinds: {},
    groupStyle: {}, // 当一个组件成为 Group 的子组件时使用
    isLock: false, // 是否锁定组件
    collapseName: '', // 编辑组件时记录当前使用的是哪个折叠面板，再次回来时恢复上次打开的折叠面板，优化用户体验
};

// 把组件数据重新分配定义
for (let i = 0, len = componentList.length; i < len; i++) {
    const item = componentList[i];
    item.style = { ...commonStyle, ...item.style };
    componentList[i] = { ...commonAttr, ...item };
}

export default componentList;
