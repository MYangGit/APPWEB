import VText from './VText/Component.vue'
import VTextAttr from './VText/Attr.vue'
import VButton from './VButton/Component.vue'
import VButtonAttr from './VButton/Attr.vue'
import VSelect from './VSelect/Component.vue'
import VSelectAttr from './VSelect/Attr.vue'
import VInput from './VInput/Component.vue'
import VInputAttr from './VInput/Attr.vue'
import VPlot from './VPlot/Component.vue'
import VPlotAttr from './VPlot/Attr.vue'
import VCheckBox from './VCheckBox/Component.vue'
import VCheckBoxAttr from './VCheckBox/Attr.vue'
import VRadio from './VRadio/Component.vue'
import VRadioAttr from './VRadio/Attr.vue'
import VTextArea from './VTextArea/Component.vue'
import VTextAreaAttr from './VTextArea/Attr.vue'
const components = {
    VText,
    VButton,
    VSelect,
    VInput,
    VPlot,
    VCheckBox,
    VRadio,
    VTextArea
};
const attrs = {
    VTextAttr,
    VButtonAttr,
    VSelectAttr,
    VInputAttr,
    VPlotAttr,
    VCheckBoxAttr,
    VRadioAttr,
    VTextAreaAttr
};

export const install = function (app) {
    Object.keys(components).forEach((key) => {
        app.component(key, components[key]);
        app.component(key + 'Attr', attrs[key + 'Attr']);
    });
};
