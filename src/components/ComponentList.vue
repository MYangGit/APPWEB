<script setup>
import { ref } from 'vue'
import componentList from '@/custom-component/component-list'; // 导入子组件数据
const activeNames = ref(['common', 'box', 'Ty', 'report'])

const types = ref([
  {
    type: 'common',
    label: '基础组件',
  }
])

const handleDragStart = (e, item) => {
  e.dataTransfer.setData(
    'index',
    componentList.findIndex((i) => i.component === item.component),
  );
}

</script>

<template>
  <div class="component-list">
    <el-collapse v-model="activeNames">
        <el-collapse-item v-for="(item, index) in types" :key="index" :title="item.label" :name="item.type">
          <!-- 为了使元素可拖动，把 draggable 属性设置为 true  默认就是true -->
          <div
              v-for="(ite, ind) in componentList.filter((i) => i.type === item.type)"
              :key="ind"
              class="list"
              :draggable="true"
              :data-index="ind"
              @dragstart="(e) => handleDragStart(e, ite)"
          >
              <!-- 子组件图标 -->
              <span class="iconfont" :class="'icon-' + ite.icon"></span>
              <label>{{ ite.label }}</label>
          </div>
        </el-collapse-item>
    </el-collapse>
  </div>
</template>

<style lang="less" scoped>
.component-list {
  // height: 65%;
  // padding: 0 10px;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  :deep(.el-collapse-item__header) {
    margin: 0 -10px 0 0;
    padding-left: 10px
  }
  :deep(.el-collapse-item__content) {
    margin: 10px 15px;
    display: grid;
    grid-gap: 10px 15px;
    grid-template-columns: repeat(auto-fill, 80px);
    grid-template-rows: repeat(auto-fill, 55px);
  }
  :deep(.el-collapse-item__arrow) {
    margin-right: 18px;
  }
  .list {
    width: 80px;
    height: 55px;
    border: 1px solid #ddd;
    cursor: grab;
    text-align: center;
    color: #333;
    padding: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    font-size: 12px;

    &:active {
      cursor: grabbing;
    }
    label {
      cursor: grab;
    }

    .iconfont {
      margin-right: 4px;
      font-size: 20px;
    }
  }
}
</style>