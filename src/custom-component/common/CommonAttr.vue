<template>
    <div class="v-common-attr">
        <el-collapse v-model="activeName" accordion @change="onChange">
            <el-collapse-item title="通用样式" name="style">
                <el-form>
                    <el-form-item v-for="({ key, label }, index) in styleKeys" :key="index" :label="label">
                        <el-slider
                            v-if="key === 'opacity'"
                            v-model="curComponent.style[key]"
                            :step="0.1"
                            :max="1"
                            show-stops>
                        </el-slider>
                        <el-color-picker
                            v-else-if="isIncludesColor(key)"
                            v-model="curComponent.style[key]"
                            show-alpha
                        ></el-color-picker>
                        <el-select v-else-if="selectKey.includes(key)" v-model="curComponent.style[key]">
                            <el-option
                                v-for="item in optionMap[key]"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            ></el-option>
                        </el-select>
                        <el-input 
                            v-else-if="isWidth(key)" 
                            v-model="curComponent.style[key]"
                            type="number"
                            min="0"
                            :max="canvasStyleData.width"
                        />
                        <el-input v-else-if="isString(key)" v-model="curComponent.style[key]"></el-input>
                        <el-input v-else v-model.number="curComponent.style[key]" type="number" />
                    </el-form-item>
                </el-form>
            </el-collapse-item>
            <el-collapse-item title="定制属性" name="design">
                <div class="v-common-design">
                    <slot></slot>
                </div>
            </el-collapse-item>
            <el-collapse-item v-if="showDevelopFunction" title="数据绑定" name="databind">
                <div class="v-common-design">
                    <div class="data-bind-item" v-for="key in getKeys(curComponent.propValue)">
                        <div class="label">{{ key }}</div>
                        <div>
                            <el-button v-if="!curComponent.dataBinds[key]" size="small" @click="bindData(key)">绑定数据</el-button>
                            <el-tag closable @close="unbindData(key)" v-else>{{ curComponent.dataBinds[key].join('.') }}</el-tag>
                        </div>
                    </div>
                </div>
            </el-collapse-item>
            <el-collapse-item title="动作绑定" v-if="showDevelopFunction && getKeys(curComponent.actionBinds).length > 0" name="actionbind">
                <div class="v-common-design">
                    <div class="data-bind-item" v-for="key in getKeys(curComponent.actionBinds)">
                        <div class="label">{{ key }}</div>
                        <div>
                            <el-button v-if="!curComponent.actionBinds[key]" size="small" @click="bindActionData(key)">绑定动作</el-button>
                            <el-tag closable @close="unbindActionData(key)" v-else>{{ curComponent.actionBinds[key] }}</el-tag>
                        </div>
                    </div>
                </div>
            </el-collapse-item>
            <el-collapse-item v-if="showDevelopFunction" title="显示状态绑定" name="visiablebind">
                <div class="v-common-design">
                    <div class="data-bind-item">
                        <el-button v-if="!(curComponent.visiable && curComponent.visiable.key)" size="small" @click="bindData('key', 'visiable')">绑定数据</el-button>
                        <el-tag closable @close="unbindData('key', 'visiable')" v-else>{{ curComponent.visiable && curComponent.visiable.key.join('.') }}</el-tag>
                    </div>
                    <div class="data-bind-item">
                        <el-input type="text" v-if="curComponent.visiable" v-model="curComponent.visiable.value" />
                    </div>
                </div>
            </el-collapse-item>
            <el-collapse-item v-if="curComponent.exposeAttr" title="组件名" name="varName">
                <div class="v-common-design">
                    <div class="data-bind-item">
                        <el-input size="small" style="margin-right: 10px;" @input="bindVarNameHasChanged = true" type="text" v-model="bindVarName" />
                        <el-button :disabled="!bindVarNameHasChanged" size="small" @click="confirmBindVarName">应用</el-button>
                    </div>
                </div>
            </el-collapse-item>
            <el-collapse-item v-if="getKeys(curComponent.actionBinds).length > 0" title="事件回调方法" name="callback">
                <div class="v-common-design">
                    <div class="v-common-design">
                        <div class="data-bind-item" v-for="key in getKeys(curComponent.actionBinds)">
                            <div class="label">{{ eventNameMap[key] }}</div>
                            <div>
                                <el-button 
                                    v-if="!curComponent.actionBinds[key]" 
                                    size="small" 
                                    @click="callbackEdit(key, 'new')"
                                >编辑</el-button>
                                <el-tag 
                                    closable 
                                    @click="callbackEdit(key, 'edit')" 
                                    @close="removeCallback(key)" 
                                    v-else
                                 >{{ curComponent.actionBinds[key] }}</el-tag>
                            </div>
                        </div>
                    </div>
                </div>
            </el-collapse-item>
        </el-collapse>

        <!-- 数据绑定弹窗 -->
        <el-dialog v-model="dataConfigShow" title="数据绑定" width="800">
            <el-cascader 
                v-model="form.bindKeys" 
                :props="{checkStrictly: true}" 
                :options="getOptions()" 
            />
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="dataConfigShow = false">Cancel</el-button>
                    <el-button type="primary" @click="handleConfirm">
                    Confirm
                    </el-button>
                </div>
            </template>
        </el-dialog>
        <!-- 动作绑定弹窗 -->
        <el-dialog v-model="actionConfigShow" title="动作绑定" width="800">
            <el-form label-position="top" label-width="auto">
                <el-form-item label="选择动作">
                    <el-select v-model="actionForm.bindKey">
                        <el-option 
                            v-for="item in getActionOptions()" 
                            :key="item" 
                            :label="item" 
                            :value="item" 
                        />
                    </el-select>
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="actionConfigShow = false">Cancel</el-button>
                    <el-button type="primary" @click="handleActionConfirm">
                    Confirm
                    </el-button>
                </div>
            </template>
        </el-dialog>
        <!-- 回调函数编写弹窗 -->
        <el-dialog v-model="callbackEditShow" title="回调函数编辑" width="800">
            <div class="languageSwitch"><LanguageSwitch/></div>
            <el-form label-position="left" label-width="auto">
                <el-form-item label="函数定义">
                    <div style="width: 100%;height: 500px;">
                        <Codemirror
                            v-model="callbackForm.code"
                            :autofocus="false"
                            :indent-with-tab="true"
                            :tab-size="2"
                            :extensions="{Julia: extensions, Python: extensionspython, Javascript: extensionsjs}[Language.cunLanguage]"
                        />
                    </div>
                </el-form-item>
            </el-form>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="callbackEditShow = false">Cancel</el-button>
                    <el-button type="primary" @click="handleCallbackConfirm">
                    Confirm
                    </el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import {
    styleData,
    textAlignOptions,
    borderStyleOptions,
    verticalAlignOptions,
    selectKey,
    optionMap,
} from '@/utils/attr';
import { rootStore } from '@/stores/rootStore';
import { mapState } from 'pinia';
import { updateVarName, updateCallback } from '@/hooks/useComponent'
import { Codemirror } from 'vue-codemirror'
import { noctisLilac } from 'thememirror'
import { julia } from "@plutojl/lang-julia";
import LanguageSwitch from '@/components/module/LanguageSwitch.vue';
import { python } from "@codemirror/lang-python";
import { javascript } from "@codemirror/lang-javascript";
import { useProgramLanguage } from '@/hooks/useProgramLanguage';

const extractKeys = (obj) => {
    let result = [];
    for (let key in obj) {
        if (typeof obj[key] === 'object' && !Array.isArray(obj[key])) {
            result.push({
                label: key,
                value: key,
                children: extractKeys(obj[key])
            });
        } else {
            result.push({
                label: key,
                value: key
            });
        }
    }
    return result;
}

const eventNameMap = {
    change: "当值更新时",
    click: "当单击时"
}

export default {
    components: { Codemirror, LanguageSwitch },
    data() {
        return {
            eventNameMap,
            optionMap,
            styleData,
            textAlignOptions,
            borderStyleOptions,
            verticalAlignOptions,
            selectKey,
            activeName: '',
            form: {
                key: '',
                bindKeys: '',
                type: 'normal'
            },
            dataConfigShow: false,
            actionConfigShow: false,
            actionForm: {
                key: '',
                bindKey: ''
            },
            bindVarName: '',
            bindVarNameHasChanged: false,
            callbackEditShow: false,
            callbackForm: {
                mode: 'new',
                key: '',
                code: ''
            },
            extensions: [julia(), noctisLilac],
            extensionspython: [python(), noctisLilac],
            extensionsjs: [javascript(), noctisLilac],
            rootStore,
        };
    },
    computed: {
        ...mapState(rootStore.usePageStore, ['canvasStyleData']),
        Language() {
            return useProgramLanguage();
        },
        styleKeys() {
            if (this.curComponent) {
                const curComponentStyleKeys = Object.keys(this.curComponent.style);
                return this.styleData.filter((item) => curComponentStyleKeys.includes(item.key));
            }

            return [];
        },
        curComponent() {
            return rootStore.dataCenter.curComponent;
        },
        showDevelopFunction() {
            return this.$route.query.mode === 'develop' || true;
        },
    },
    watch: {
        curComponent() {
            if (this.curComponent.exposeAttr) {
                this.bindVarName = this.curComponent.componentStateName
            }
        },
        // 监听language变化 更新回调函数内容
        Language: {
            handler(val) {
                if(this.callbackForm.mode === 'edit') {
                    let actionKey = rootStore.dataCenter.curComponent.actionBinds[this.callbackForm.key]
                    let code = rootStore.dataConfig.actionSet[actionKey]
                    let actionKeySuffix = actionKey.split('@').pop();
                    let languageSwitch = {julia: 'Julia', python: 'Python'}[actionKeySuffix] || 'Javascript'
                    if (languageSwitch != val.cunLanguage) {
                        this.callbackForm.code = ''
                    } else {
                        this.callbackForm.code = code
                    }
                }
            },
            deep: true
        }
    },
    created() {
        this.activeName = this.curComponent.collapseName || 'design';
        if (this.curComponent.exposeAttr) {
            this.bindVarName = this.curComponent.componentStateName
        }
    },
    methods: {
        onChange() {
            this.curComponent.collapseName = this.activeName;
        },

        isIncludesColor(str) {
            return str.toLowerCase().includes('color');
        },
        isString(str) {
            return ['fixedheight', 'fixedwidth'].includes(str.toLowerCase());
        },
        isWidth(str) {
            return ['width'].includes(str.toLowerCase());
        },
        bindData (key, type) {
            this.form.bindKeys = ''
            this.form.key = key
            if (type) this.form.type = type
            this.dataConfigShow = true
        },
        bindActionData (key) {
            this.actionForm.bindKey = ''
            this.actionForm.key = key
            this.actionConfigShow = true
        },
        callbackEdit (key, mode) {
            this.callbackForm.mode = mode
            this.callbackForm.key = key
            if (mode === 'edit') {
                let actionKey = rootStore.dataCenter.curComponent.actionBinds[this.callbackForm.key]
                let actionKeySuffix = actionKey.split('@').pop();
                let languageSwitch = {julia: 'Julia', python: 'Python'}[actionKeySuffix] || 'Javascript'
                if (languageSwitch !== this.Language.cunLanguage) {
                   this.Language.setCunLanguage(languageSwitch)
                }
                let code = rootStore.dataConfig.actionSet[actionKey]
                this.callbackForm.code = code
            } else {
                this.callbackForm.code = ''
            }
            this.callbackEditShow = true
        },
        handleConfirm () {
            if (this.form.type === 'visiable') {
                rootStore.dataCenter.curComponent.visiable[this.form.key] = this.form.bindKeys
            }
            if (this.form.type === 'normal') {
                rootStore.dataCenter.curComponent.dataBinds[this.form.key] = this.form.bindKeys
            }
            this.dataConfigShow = false
        },
        handleActionConfirm () {
            rootStore.dataCenter.curComponent.actionBinds[this.actionForm.key] = this.actionForm.bindKey
            this.actionConfigShow = false
        },
        handleCallbackConfirm () {
            updateCallback(this.callbackForm, this.Language.cunLanguage)
            this.callbackEditShow = false
        },
        unbindData(key, type = 'normal') {
            if (type === 'visiable') {
                rootStore.dataCenter.curComponent.visiable[this.form.key] = ''
            }
            if (type === 'normal') {
                delete rootStore.dataCenter.curComponent.dataBinds[key]
            }
        },
        unbindActionData (key) {
            rootStore.dataCenter.curComponent.actionBinds[key] = ''
        },
        removeCallback (key) {
            rootStore.dataConfig.deleteAction(rootStore.dataCenter.curComponent.actionBinds[key])
            rootStore.dataCenter.curComponent.actionBinds[key] = ''
        },
        confirmBindVarName () {
            updateVarName(this.bindVarName)
            this.bindVarNameHasChanged = false;
        },
        getOptions () {
            let options = extractKeys(rootStore.dataConfig.stateSet);
            return options;
        },
        getActionOptions () {
            return Object.keys(rootStore.dataConfig.actionSet)
        },
        getKeys (obj) {
            if (typeof obj === 'object') {
                return Object.keys(obj);
            } else {
                return ['value'];
            }
        }
    },
};
</script>

<style lang="less">
.v-common-attr {
    .el-input-group__prepend {
        padding: 0 10px;
    }
}
.languageSwitch {
    position: absolute;
    top: 15px;
    right: 50px;
}
.v-common-design {
    padding: 10px;
}

.el-collapse-item__header {
    padding: 0 10px;
    margin: 0 0;
}

.data-bind-item {
    display: flex;
    margin-bottom: 5px;
    justify-content: space-between;
    .label {
        width: 70px;
    }
}
</style>
