<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="label">
                    <el-input v-model="curComponent.propValue.label" size="small" />
                </el-form-item>
                <el-form-item label="单选项列表">
                    <el-button size="small" @click="add">+</el-button>
                    <el-form v-for="item, index in options" :key="index" :inline="true" label-width="40px" size="small" style="padding: 10px 0">
                        <el-form-item label="label" style="margin-bottom: 0;">
                            <el-input v-model="item.label" style="width: 50px" />
                        </el-form-item>
                        <el-form-item label="value" style="margin-bottom: 0;">
                            <el-input v-model="item.value" style="width: 50px" />
                        </el-form-item>
                        <el-form-item label="" style="margin-bottom: 0; margin-right: 0;">
                            <el-button @click="deleteRow(index)">-</el-button>
                        </el-form-item>
                    </el-form>
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
            return rootStore.dataCenter.curComponent.propValue.options
        },
    },
    methods: {
        add() {
            this.options.push({
                label: '',
                value: '',
            })
        },
        deleteRow(index) {
            this.options.splice(
                index,
                1,
            )
        },
    },
}
</script>
