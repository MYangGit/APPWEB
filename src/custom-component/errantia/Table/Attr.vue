<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <span>对齐方式：</span>
                <el-radio-group v-model="curComponent.propValue.textAlign" class="ml-4">
                    <el-radio value="left" size="large">靠左</el-radio>
                    <el-radio value="center" size="large">居中</el-radio>
                    <el-radio value="right" size="large">靠右</el-radio>
                </el-radio-group>
                <el-form-item label="显示边框：">
                    <el-checkbox v-model="curComponent.propValue.showBorder" size="small" />
                </el-form-item>
                <el-form-item label="可选中行：">
                    <el-checkbox v-model="curComponent.propValue.activeClickRow" size="small" />
                </el-form-item>
                <el-form-item label="操作列：">
                    <el-checkbox 
                        v-model="curComponent.propValue.showOperate" 
                        size="small"
                        @change="handleShowOperate"
                    />
                </el-form-item>
            </el-form>
        </CommonAttr>
    </div>
</template>

<script>
import CommonAttr from '@/custom-component/common/CommonAttr.vue'
import { rootStore } from '@/stores/rootStore';

export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent
        },
        options() {
            return rootStore.dataCenter.curComponent.propValue.columns
        },
    },
    methods: {
        handleShowOperate(val) {
            if (val) {
                this.curComponent.propValue.columns.push({
                    title: '操作',
                    key: 'operate',
                    slot: 'operate'
                })
            } else {
                this.curComponent.propValue.columns = this.curComponent.propValue.columns.filter(item => item.key !== 'operate')
            }
        }
    }
}
</script>
