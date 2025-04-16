<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="禁用">
                    <el-switch v-model="curComponent.propValue.disabled" size="small" />
                </el-form-item>
                <el-form-item label="匹配内容选中：">
                    <el-input  v-model="curComponent.propValue.activateText"  size="small" />
                </el-form-item>
                <el-form-item label="value">
                    <el-input  v-model="curComponent.propValue.value"  size="small" />
                </el-form-item>
                <el-form-item label="树形节点key">
                    <el-input  v-model="curComponent.propValue.nodeKey"  size="small" />
                </el-form-item>
                <el-form-item label="树形列表">
                    <el-button size="small" @click="add">+</el-button>
                </el-form-item>
                <el-form v-for="item, index in options" :key="index" :inline="true" label-width="40px" size="small" style="padding: 10px 0">
                    <el-form-item label="id" style="margin-bottom: 0;">
                        <el-input v-model="item.id"  />
                    </el-form-item>
                    <el-form-item label="label" style="margin-bottom: 0;">
                        <el-input v-model="item.label"  />
                    </el-form-item>
                    <el-form-item label="value" style="margin-bottom: 10px;">
                        <el-input v-model="item.value" />
                    </el-form-item>
                    <el-button @click="deleteRow(index)">x</el-button>
                    <el-button size="small" @click="addChildren(item, index)">添加子项</el-button>
                    <el-form-item style="margin-left: 20px;">
                        <el-form v-for="childitem, childindex in item.children" :key="childindex" :inline="true" label-width="40px" size="small" style="padding: 10px 0">
                            <el-form-item label="id" style="margin-bottom: 0;">
                                <el-input v-model="childitem.id"  />
                            </el-form-item>
                            <el-form-item label="label" style="margin-bottom: 0;">
                                <el-input v-model="childitem.label"  />
                            </el-form-item>
                            <el-form-item label="value" style="margin-bottom: 10px;">
                                <el-input v-model="childitem.value" />
                            </el-form-item>
                            <el-button @click="deleteRowChildren(item, childindex)">-</el-button>
                            <el-button size="small" @click="addChildren(childitem, childindex)">添加子项</el-button>
                            <el-form-item style="margin-left: 20px;">
                                <el-form v-for="childitem1, childindex1 in childitem.children" :key="childindex1" :inline="true" label-width="40px" size="small" style="padding: 10px 0">
                                    <el-form-item label="id" style="margin-bottom: 0;">
                                        <el-input v-model="childitem1.id"  />
                                    </el-form-item>
                                    <el-form-item label="label" style="margin-bottom: 0;">
                                        <el-input v-model="childitem1.label"  />
                                    </el-form-item>
                                    <el-form-item label="value" style="margin-bottom: 10px;">
                                        <el-input v-model="childitem1.value" />
                                    </el-form-item>
                                    <el-button @click="deleteRowChildren(childitem,childindex1)">-</el-button>
                                </el-form>
                            </el-form-item>
                        </el-form>
                    </el-form-item>
                    <el-divider />
                </el-form>
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
                id: '',
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
        addChildren(item) {
            if (!item.children) {
                item.children = []
            }
            item.children.push({
                id: '',
                label: '',
                value: '',
            })
        },
        deleteRowChildren(item, index) {
            item.children.splice(
                index,
                1,
            )
        },
    },
}
</script>
