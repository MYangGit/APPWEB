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
                        <el-input v-else-if="isString(key)" v-model="curComponent.style[key]"></el-input>
                        <el-input v-else v-model.number="curComponent.style[key]" type="number" />
                    </el-form-item>
                </el-form>
            </el-collapse-item>
            <Linkage v-if="curComponent.linkage"></Linkage>
            <el-collapse-item title="定制属性" name="design">
                <div class="v-common-design">
                    <slot></slot>
                </div>
            </el-collapse-item>
            <el-collapse-item title="数据绑定" name="databind">
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
            <el-collapse-item title="动作绑定" v-if="getKeys(curComponent.actionBinds).length > 0" name="actionbind">
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
            <el-collapse-item title="显示状态绑定" name="visiablebind">
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
        </el-collapse>
        <el-dialog v-model="dataConfigShow" title="数据绑定" width="800">
            <el-cascader v-model="form.bindKeys" :props="{checkStrictly: true}" :options="getOptions()" />
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="dataConfigShow = false">Cancel</el-button>
                    <el-button type="primary" @click="handleConfirm">
                    Confirm
                    </el-button>
                </div>
            </template>
        </el-dialog>
        <el-dialog v-model="actionConfigShow" title="动作绑定" width="800">
            <el-select v-model="actionForm.bindKey">
                <el-option v-for="item in getActionOptions()" :key="item" :label="item" :value="item"></el-option>
            </el-select>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="actionConfigShow = false">Cancel</el-button>
                    <el-button type="primary" @click="handleActionConfirm">
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
import Linkage from './Linkage.vue';
import { rootStore } from '@/stores/rootStore';

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

export default {
    components: { Linkage },
    data() {
        return {
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
            rootStore,
        };
    },
    computed: {
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
    },
    created() {
        this.activeName = this.curComponent.collapseName || 'design';
    },
    methods: {
        onChange() {
            this.curComponent.collapseName = this.activeName;
        },

        isIncludesColor(str) {
            return str.toLowerCase().includes('color');
        },
        isString(str) {
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
        unbindData(key, type = 'normal') {
            if (type === 'visiable') {
                rootStore.dataCenter.curComponent.visiable[this.form.key] = ''
            }
            if (type === 'normal') {
                delete rootStore.dataCenter.curComponent.dataBinds[key]
            }
        },
        unbindActionData (key) {
            delete rootStore.dataCenter.curComponent.actionBinds[key]
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
    .label {
        width: 70px;
    }
}
</style>
