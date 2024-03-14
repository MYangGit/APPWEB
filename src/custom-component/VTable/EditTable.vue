<template>
    <div class="edit-table">
        <el-table :data="tableData" style="width: 100%" border>
            <el-table-column v-for="item in columns" :key="item.field" :prop="item.field" :label="item.label">
                <template slot-scope="scope">
                    <el-input
                        v-if="curTd === scope.$index + ',' + item.field"
                        v-model="scope.row[item.field]"
                        v-focus
                        @blur="onBlur"
                    ></el-input>
                    <div v-else style="min-height: 23px" @click="onClick(scope.$index, item.field)">{{ scope.row[item.field] }}</div>
                </template>
            </el-table-column>
        </el-table>
        <div>
            <button class="button" @click="addRow">添加新行</button>
            <button class="button" @click="centerDialogVisible = true">添加新列</button>
            <button class="button" @click="deleteRow">删除行</button>
            <button class="button" @click="deleteCol">删除列</button>
        </div>
        <el-dialog
            title="添加新列"
            :visible="centerDialogVisible"
            width="500px"
            style="height: fit-content"
            @close="handleCloseModal"
        >
            <el-form>
                <el-form-item label="列名称">
                    <el-input v-model="column.label"></el-input>
                </el-form-item>
                <el-form-item label="绑定字段">
                    <el-input v-model="column.field"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="handleCloseModal">取 消</el-button>
                <el-button type="primary" @click="addCol">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { rootStore } from '@/stores/rootStore';
export default {
    directives: {
        focus: {
            // 指令的定义
            inserted(el) {
                // 聚焦元素
                el.querySelector('input').focus()
            },
        },
    },
    data() {
        return {
            column: {
                label: ' ',
                field: ' ',
            },
            centerDialogVisible: false,
            curTd: '',
            preCurTd: '', // 失焦时 curTd 值为空，这时删除会读不到值，因此用这个变量来代替，用于删除行列
        }
    },
    computed: {
        tableData() {
            return rootStore.dataCenter.curComponent.propValue.data
        },
        columns() {
            return rootStore.dataCenter.curComponent.propValue.columns
        },
    },
    methods: {
        handleCloseModal() {
            this.centerDialogVisible = false
        },
        onClick(index, col) {
            this.curTd = index + ',' + col
            this.preCurTd = this.curTd
        },

        onBlur() {
            this.curTd = ''
        },

        deleteRow() {
            if (!this.preCurTd) {
                this.$message.error('请先选择要删除的行')
                return
            }

            const row = this.preCurTd.split(',')[0]
            this.tableData.splice(row, 1)
        },

        addRow() {
            this.tableData.push(
                this.columns.reduce((obj, i) => {
                    obj[i.field] = ''
                    return obj
                }, {}),
            )
        },

        addCol() {
            this.columns.push({ ...this.column })
            this.handleCloseModal()
        },

        deleteCol() {
            if (!this.preCurTd) {
                this.$message.error('请先选择要删除的列')
                return
            }

            const col = this.preCurTd.split(',')[1]
            this.columns.splice(
                this.columns.findIndex((i) => i.field === col),
                1,
            )
        },
    },
}
</script>

<style lang="less" scoped>
.edit-table {
    overflow: auto;
    margin-bottom: 8px;

    & > div {
        margin-top: 18px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;

        .button {
            cursor: pointer;
            background: #fff;
            border: 1px solid #dcdfe6;
            color: #606266;
            text-align: center;
            box-sizing: border-box;
            outline: 0;
            margin: 0;
            font-weight: 500;
            padding: 4px 5px;
            font-size: 14px;
            border-radius: 4px;
            margin-bottom: 10px;

            &:hover {
                background: #ecf5ff;
                color: #409eff;
            }
        }
    }

    table {
        border-collapse: collapse;
        word-break: break-all;
        word-wrap: break-word;
        text-align: center;
        font-size: 12px;

        td {
            border: 1px solid #ebeef5;
            height: 40px;
            min-width: 60px;
            max-width: 80px;
            padding: 10px;
        }
    }

    .selected {
        background: #ecf5ff;
        color: #409eff;
    }
}
</style>
