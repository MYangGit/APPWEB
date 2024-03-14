<template>
    <el-dialog :title="title" :visible="show" width="50%" @close="hide">
        <slot></slot>
        <span slot="footer" class="dialog-footer" v-if="showBtns">
            <el-button @click="hide">取 消</el-button>
            <el-button type="primary" @click="submit">确定</el-button>
        </span>
    </el-dialog>
</template>

<script>
export default {
    props: {
        show: {
            type: Boolean,
            default: false,
        },
        title: {
            type: String,
            default: '',
        },
        showBtns: {
            type: Boolean,
            default: true,
        },
    },
    methods: {
        hide() {
            this.$emit('close')
        },

        stopPropagation(e) {
            e.stopPropagation()
        },

        submit() {
            this.$emit('submit')
            this.hide()
        },
    },
}
</script>

<style lang="less" scoped>
.modal-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1001;

    .modal {
        width: 640px;
        margin: 200px auto;
        background: #fff;
        height: 550px;
    }
}
</style>
