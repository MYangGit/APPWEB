<template>
    <div class="attr-list">
        <CommonAttr>
            <div class="attr-title">属性</div>
            <el-form>
                <el-form-item label="是否显示播放按钮">
                    <el-radio-group v-model="propValue.showPlay">
                        <el-radio :value="true">是</el-radio>
                        <el-radio :value="false">否</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="类型">
                    <el-radio-group v-model="propValue.props.type">
                        <el-radio-button value="line">line</el-radio-button>
                        <el-radio-button value="bar">bar</el-radio-button>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="标题">
                    <el-input v-model="propValue.title" />
                </el-form-item>
                <el-form-item label="标题颜色">
                    <el-color-picker v-model="propValue.titleColor" />
                </el-form-item>
                <el-form-item label="标题大小">
                    <el-input-number v-model="propValue.titleSize" />
                </el-form-item>
                <el-form-item label="标题对齐方式">
                    <el-select v-model="propValue.titleAlign">
                        <el-option
                            v-for="item in textAlignOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="自动触发联动">
                    <el-radio-group v-model="propValue.autoPlay">
                        <el-radio :value="true">是</el-radio>
                        <el-radio :value="false">否</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="是否循环播放">
                    <el-radio-group v-model="propValue.circulate">
                        <el-radio :value="true">是</el-radio>
                        <el-radio :value="false">否</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="触发周期（ms）">
                    <el-input-number v-model="propValue.autoPlayTime" />
                </el-form-item>
            </el-form>
        </CommonAttr>
    </div>
</template>

<script>
import {
    textAlignOptions,
} from '@/utils/attr';
import CommonAttr from '@/custom-component/common/CommonAttr.vue'
import { rootStore } from '@/stores/rootStore';

export default {
    components: { CommonAttr },
    data() {
        return {
            textAlignOptions,
        }
    },
    computed: {
        propValue() {
            return rootStore.dataCenter.curComponent.propValue;
        },
    },
};
</script>
