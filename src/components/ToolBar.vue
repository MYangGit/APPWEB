<!-- 界面上方工具栏 -->
<template>
  <div class="toolbar-wrap">
    <div class="toolbar">
      <div class="tool-item" v-for="item in actions" :key="item.title" @click="item.action">
        <img :src="item.icon" class="item-icon" />
        <p class="item-title">{{ item.title }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
  // import generateID from '@/utils/generateID';
  // import toast from '@/utils/toast';
  // import localforage from 'localforage';
  // import { deepCopy, $, generatePassword, reg, exportJson, getQueryVariable } from '@/utils/utils';
  // import { divide, multiply } from 'mathjs';

  import { actions } from '@/config/toolbar'
</script>

<style lang="less" scoped>
.toolbar-wrap {
  display: flex;
  border-bottom: 1px solid #ddd;
  align-items: center;
}
.toolbar {
  padding: 15px 10px;
  white-space: nowrap;
  overflow-x: auto;
  background: #fff;
  display: flex;
  font-size: 12px;

  .tool-item {
    text-align: center;
    padding: 2px 6px;
    border: 1px solid transparent;
    cursor: pointer;

    .item-icon {
      width: 35px;
      height: 35px;
      display: block;
    }
    .item-title {
      margin: 2px 0;
      display: inline-block;
    }
    &:hover {
      background: #e5e5e5;
      border: 1px solid #e5e5e5;
    }
  }

  .canvas-config {
    display: inline-block;
    margin-left: 10px;
    font-size: 14px;
    color: #606266;

    input {
      width: 50px;
      margin-left: 4px;
      outline: none;
      padding: 0 5px;
      border: 1px solid #ddd;
      color: #606266;
    }

    span {
      margin-left: 10px;
    }
  }

  .insert {
    display: inline-block;
    line-height: 1;
    white-space: nowrap;
    cursor: pointer;
    background: #fff;
    border: 1px solid #dcdfe6;
    color: #606266;
    text-align: center;
    box-sizing: border-box;
    outline: 0;
    margin: 0;
    transition: 0.1s;
    font-weight: 500;
    padding: 9px 15px;
    font-size: 12px;
    border-radius: 3px;
    margin-left: 10px;

    &:active {
      color: #3a8ee6;
      border-color: #3a8ee6;
      outline: 0;
    }

    &:hover {
      background-color: #ecf5ff;
      color: #3a8ee6;
    }
  }
  .import-file {
    position: relative;
    #fileId {
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      opacity: 0;
    }
  }
}
.app-name {
  width: 200px;
}
</style>
