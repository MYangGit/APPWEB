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
        </el-collapse>
        <el-dialog v-model="dataConfigShow" title="数据绑定" width="800">
            <el-cascader v-model="form.bindKeys" :options="getOptions(rootStore.dataConfig.stateSet)" />
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="dataConfigShow = false">Cancel</el-button>
                    <el-button type="primary" @click="handleConfirm">
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
                bindKeys: ''
            },
            dataConfigShow: false,
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
        bindData (key) {
            this.form.bindKeys = ''
            this.form.key = key
            this.dataConfigShow = true
        },
        handleConfirm () {
            rootStore.dataCenter.curComponent.dataBinds[this.form.key] = this.form.bindKeys
            this.dataConfigShow = false
        },
        unbindData(key) {
            delete rootStore.dataCenter.curComponent.dataBinds[key]
        },
        getOptions () {
            let options = extractKeys(rootStore.dataConfig.stateSet);
            return options;
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
