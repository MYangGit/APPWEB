<template>
    <div class="no-position">
        <el-table :data="propValue.data" style="width: 100%" :border="propValue.border" :stripe="propValue.stripe">
            <el-table-column v-for="item in propValue.columns" :key="item.field" :prop="item.field" :label="item.label">
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
import request from '@/utils/request';
import OnEvent from '../common/OnEvent';

export default {
    extends: OnEvent,
    props: {
        propValue: {
            type: Object,
            default: () => {},
        },
        request: {
            type: Object,
            default: () => {},
        },
        element: {
            type: Object,
            default: () => {},
        },
    },
    data() {
        return {
            cancelRequest: null,
        };
    },
    created() {
        if (this.request) {
            this.cancelRequest = request(this.request, this.propValue, 'data');
        }
    },
    beforeDestroy() {
        // this.request && this.cancelRequest();
    },
    methods: {
        updateData() {
            if (this.cancelRequest) {
                // this.request && this.cancelRequest();
                this.cancelRequest = null;
            } else if (this.request) {
                this.cancelRequest = request(this.request, this.propValue, 'data');
            }
        },
    },
};
</script>

<style lang="less" scoped>
.v-table {
    border-collapse: collapse;
    table-layout: fixed;
    word-break: break-all;
    word-wrap: break-word;

    td {
        border: 1px solid #ebeef5;
        height: 40px;
        width: 60px;
        padding: 10px;
    }

    .bold {
        font-weight: bold;
    }

    .stripe {
        background-color: #fafafa;
    }
}
</style>
