<template>
  <erDialog 
    :title="confirmBoxState.title"
    :width="confirmBoxState.width + 'px'"
    :isVisible="confirmBoxState.isShow"
    :okBtn="confirmBoxState.sureText"
    :cancelBtn="confirmBoxState.cancelText"
    :outStyleBody="{padding: '10px'}"
    @close="cancel"
    @cancel="cancel"
    @confirm="sure"
  >
    <div v-if="isEmpty(confirmBoxState.message)" :style="{ height: confirmBoxState.height + 'px' }">暂无数据</div>
    <div v-else :style="{ height: confirmBoxState.height + 'px' }" class="custom-content">{{confirmBoxState.message}}</div>
  </erDialog>
</template>

<script setup>
import { rootStore } from '@/stores/rootStore';
import { computed } from 'vue';
import { isEmpty } from '@/utils/utils'

const confirmBoxState = computed(() => rootStore.confirmBox.confirmBoxState)

const sure = () => {
  rootStore.confirmBox.resolveConfirmBox()
}

const cancel = () => {
  rootStore.confirmBox.rejectConfirmBox()
}

</script>

<style lang="less" scoped>

.confirm-box-backdrop {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.confirm-box {
  width: 400px;
  box-shadow: 0px 2px 4px 2px rgba(101,95,95,0.5);
  border-radius: 8px;
  border: 1px solid #B6B6B6;
  background-color: #F3F3F3;
}

.title-bar {
  width: 100%;
  height: 30px;
  background: #F7FCFF;
  border-radius: 8px;
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  display: flex;
  align-items: center;
  position: relative;
  padding: 0 15px;
  .title {
    flex: 1;
  }
  .close {
    width: 20px;
    height: 20px;
    position: absolute;
    right: 0;
    top: 3px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
  }
}

.message-w {
  font-size: 12px;
  font-weight: 400;
  margin: 10px 15px;
  border-radius: 8px;
  padding: 10px 0;
  font-size: 12px;
}

.btns-w {
  display: flex;
  margin-bottom: 10px;
  justify-content: right;
  margin: 10px 15px;
  .btn {
    width: 107px;
    height: 28px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    color: #222222;
    border: 1px solid #DBDBDB;
    justify-content: center;
    margin-left: 10px;
    cursor: pointer;
  }

  .btn:hover {
    background-color: #F7FCFF;
  }
}

.custom-content {
  display: flex;
  flex-direction: column;
  font-size: 14px;
  color: #333;
  line-height: 1.5;
  overflow-y: scroll;
  word-wrap: break-word; 
  overflow-wrap: break-word;
}
</style>
