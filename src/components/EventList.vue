<template>
    <div class="event-list">
        <div class="div-events">
            <el-button @click="isShowEvent = true">添加事件</el-button>
            <div>
                <el-tag v-for="event in Object.keys(curComponent.events)" :key="event" closable @close="removeEvent(event)">
                    {{ curComponent.events[event].label }}
                </el-tag>
            </div>
        </div>

        <!-- 选择事件 -->
        <Modal v-model="isShowEvent" title="选择事件" @submit="submit" @close="isShowEvent = false">
            <el-tabs v-model="eventActiveName">
                <el-tab-pane v-for="item in eventList" :key="item.key" :label="item.label" :name="item.key" style="padding: 20px">
                    <el-input
                        v-if="item.key == 'redirect'"
                        v-model="item.param"
                        type="textarea"
                        placeholder="请输入完整的 URL"
                        @keydown.native.stop
                    />
                    <el-input
                        v-if="item.key == 'message'"
                        v-model="item.param"
                        type="textarea"
                        placeholder="请输入要提示的内容"
                        @keydown.native.stop
                    />
                    <el-input
                        v-if="item.key == 'js'"
                        v-model="item.param"
                        :rows="8"
                        type="textarea"
                        placeholder="请输入自定义的JS"
                        @keydown.native.stop
                    />
                    <!-- <el-button style="margin-top: 20px" @click="addEvent(item.key, item.param)">确定</el-button> -->
                </el-tab-pane>
            </el-tabs>
        </Modal>
    </div>
</template>

<script>
import { mapState } from 'pinia'
import Modal from '@/components/Modal'
import { eventList } from '@/utils/events'
import { rootStore } from '@/stores/rootStore'

export default {
    components: { Modal },
    data() {
        return {
            isShowEvent: false,
            eventURL: '',
            eventActiveName: 'redirect',
            eventList,
        }
    },
    mounted() {
        this.eventList.forEach(item => {
            if (this.curComponent.events[item.key]) {
                item.param = this.curComponent.events[item.key].param;
            } else {
                item.param = '';
            }
        })
    },
    computed: mapState(rootStore.useDataCenterStore, ['curComponent']),
    watch: {
        curComponent() {
            this.eventList.forEach(item => {
                if (this.curComponent.events[item.key]) {
                    item.param = this.curComponent.events[item.key].param;
                } else {
                    item.param = '';
                }
            })
        },
    },
    methods: {
        addEvent(event, param) {
            this.isShowEvent = false
            rootStore.dataCenter.addEvent({ event, param })
        },

        submit() {
            const item = this.eventList.filter(i => i.key === this.eventActiveName);
            this.isShowEvent = false;
            rootStore.dataCenter.addEvent({ event: item[0].key, param: item[0].param, label: item[0].label })
        },

        removeEvent(event) {
            rootStore.dataCenter.removeEvent(event)
        },
    },
}
</script>

<style lang="less" scoped>
.event-list {
    .div-events {
        text-align: center;
        padding: 0 20px;

        .el-button {
            width: 100%;
            display: inline-block;
            margin-bottom: 10px;
        }

        .el-tag {
            width: 50%;
            margin: auto;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            :deep(.el-tag__content) {
                flex: 1;
                text-align: center;
            }
        }
    }
}
</style>
