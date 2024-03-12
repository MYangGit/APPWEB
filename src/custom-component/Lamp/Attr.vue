<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="警戒值">
                    <el-input-number v-model="propValue.warningValue" />
                </el-form-item>
                <el-form-item label="警戒颜色">
                    <el-color-picker v-model="propValue.warningColor" />
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
}
</script>
