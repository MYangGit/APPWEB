<template>
    <div class="attr-list">
        <CommonAttr>
            <div class="attr-title">仪表盘属性</div>
            <el-form>
                <el-form-item label="是否展示进度条">
                    <el-radio-group v-model="propValue.isShowProgress">
                        <el-radio :value="true">是</el-radio>
                        <el-radio :value="false">否</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="是否展示刻度">
                    <el-radio-group v-model="propValue.isShowTick">
                        <el-radio :value="true">是</el-radio>
                        <el-radio :value="false">否</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="变量单位">
                    <el-input v-model="propValue.valueUnit" />
                </el-form-item>
                <el-form-item label="刻度字体大小">
                    <el-input-number v-model="propValue.labelFontSize" />
                </el-form-item>
                <el-form-item label="刻度字体颜色">
                    <el-color-picker v-model="propValue.labelColor" />
                </el-form-item>
                <el-form-item label="值字体大小">
                    <el-input-number v-model="propValue.valueFontSize" />
                </el-form-item>
                <el-form-item label="值字体颜色">
                    <el-color-picker v-model="propValue.valueColor" />
                </el-form-item>
                <el-form-item label="开始角度">
                    <el-input-number v-model="propValue.startAngle" />
                </el-form-item>
                <el-form-item label="截止角度">
                    <el-input-number v-model="propValue.endAngle" />
                </el-form-item>
                <el-form-item label="最小值">
                    <el-input-number v-model="propValue.min" />
                </el-form-item>
                <el-form-item label="最大值">
                    <el-input-number v-model="propValue.max" />
                </el-form-item>
                <el-form-item label="警戒值">
                    <el-input-number v-model="propValue.warningValue" />
                </el-form-item>
                <el-form-item label="保留小数位">
                    <el-input-number v-model="propValue.floatUnit" />
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
