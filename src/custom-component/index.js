import VText from './VText/Component.vue'
import VTextAttr from './VText/Attr.vue'
import VButton from './VButton/Component.vue'
import VButtonAttr from './VButton/Attr.vue'
import VSelect from './VSelect/Component.vue'
import VSelectAttr from './VSelect/Attr.vue'
import VInput from './VInput/Component.vue'
import VInputAttr from './VInput/Attr.vue'
import VHtml from './VHtml/Component.vue'
import VHtmlAttr from './VHtml/Attr.vue'
import VPlot from './VPlot/Component.vue'
import VPlotAttr from './VPlot/Attr.vue'
import VCheckBox from './VCheckBox/Component.vue'
import VCheckBoxAttr from './VCheckBox/Attr.vue'
import VRadio from './VRadio/Component.vue'
import VRadioAttr from './VRadio/Attr.vue'
import VTextArea from './VTextArea/Component.vue'
import VTextAreaAttr from './VTextArea/Attr.vue'
import VPanel from './VPanel/Component.vue'
import VPanelAttr from './VPanel/Attr.vue'
import VFlexPanel from './VFlexPanel/Component.vue'
import VFlexPanelAttr from './VFlexPanel/Attr.vue'
import VTabs from './VTabs/Component.vue'
import VTabsAttr from './VTabs/Attr.vue'
import ErPlot from './errantia/Plot/Component.vue'
import ErPlotAttr from './errantia/Plot/Attr.vue'
import ErTable from './errantia/Table/Component.vue'
import ErTableAttr from './errantia/Table/Attr.vue'
import ErInput from './errantia/Input/Component.vue'
import ErInputAttr from './errantia/Input/Attr.vue'
import ErStatusBar from './errantia/StatusBar/Component.vue'
import ErStatusBarAttr from './errantia/StatusBar/Attr.vue'
import ErLayout from './errantia/Layout/Component.vue'
import ErLayoutAttr from './errantia/Layout/Attr.vue'
import ErCollapse from './errantia/Collapse/Component.vue'
import ErCollapseAttr from './errantia/Collapse/Attr.vue'
const components = {
    VText,
    VButton,
    VSelect,
    VInput,
    VHtml,
    VPlot,
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
    ErCollapse
};
const attrs = {
    VTextAttr,
    VButtonAttr,
    VSelectAttr,
    VInputAttr,
    VHtmlAttr,
    VPlotAttr,
    VCheckBoxAttr,
    VRadioAttr,
    VTextAreaAttr,
    ErTableAttr,
    ErInputAttr,
    VPanelAttr,
    VFlexPanelAttr,
    VTabsAttr,
    ErPlotAttr,
    ErStatusBarAttr,
    ErLayoutAttr,
    ErCollapseAttr
}

export const install = function (app) {
    Object.keys(components).forEach((key) => {
        app.component(key, components[key]);
        app.component(key + 'Attr', attrs[key + 'Attr']);
    });
};
