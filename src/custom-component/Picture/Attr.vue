<template>
    <div class="attr-list">
        <CommonAttr>
            <el-form>
                <el-form-item label="镜像翻转">
                    <div style="clear: both">
                        <el-checkbox v-model="curComponent.propValue.flip.horizontal" label="horizontal">水平翻转</el-checkbox>
                        <el-checkbox v-model="curComponent.propValue.flip.vertical" label="vertical">垂直翻转</el-checkbox>
                    </div>
                </el-form-item>
                <el-form-item label="上传图片">
                    <el-upload class="upload-demo" drag action="#" :multiple="false" :before-upload="beforeUpload" accept=".png, .jpg, .jpeg, .svg, .jpg">
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                    </el-upload>
                </el-form-item>
                <el-form-item label="是否上传到服务器">
                    <div style="clear: both">
                        <el-radio v-model="curComponent.propValue.isUpload" :value="true">是</el-radio>
                        <el-radio v-model="curComponent.propValue.isUpload" :value="false">否</el-radio>
                    </div>
                </el-form-item>
            </el-form>
        </CommonAttr>
    </div>
</template>

<script>
import CommonAttr from '@/custom-component/common/CommonAttr.vue'
import { rootStore } from '@/stores/rootStore';
import { fileToBase64 } from '@/utils/utils'
import request from '@/utils/request';

export default {
    components: { CommonAttr },
    computed: {
        curComponent() {
            return rootStore.dataCenter.curComponent;
        },
    },
    methods: {
        beforeUpload(file) {
            if (this.curComponent.propValue.isUpload) {
                const formData = new FormData();
                formData.append('bizPath', 'project');
                formData.append('file', file);
                request({
                    url: this.curComponent.request.url,
                    method: this.curComponent.request.method,
                    data: formData,
                }).then((res) => {
                    if (res.data.code == 0) {
                        this.curComponent.propValue.url = (this.curComponent.request.url.includes('http') ? this.curComponent.request.url.slice(0, this.curComponent.request.url.indexOf('/', 9)) : '') + res.data.data;
                    } else {
                        this.$message.warning('上传失败');
                    }
                });
            } else {
                fileToBase64(file).then(res => {
                    this.curComponent.propValue.url = res;
                })
            }
            return false;
        },
    },
}
</script>
