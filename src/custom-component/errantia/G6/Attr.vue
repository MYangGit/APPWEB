<template>
  <div class="attr-list">
    <CommonAttr>
      <el-form>
        <el-form-item label="匹配内容选中：">
          <el-input v-model="curComponent.propValue.funParam" size="small" />
        </el-form-item>
        <el-form-item label="节点配置：">
          <el-button size="small" @click="handAddCollapse">+</el-button>
        </el-form-item>
        <el-collapse>
          <el-collapse-item
            v-for="(item, index) in nodesOptions"
            :key="item.id"
            :name="item.id"
          >
            <template #title>
              <el-icon
                v-if="item.name !== '1'"
                class="header-icon"
                @click.stop="handDelete(index)"
              >
                <CircleClose />
              </el-icon>
              面板{{ item.id }}
            </template>
            <el-form>
              <br />
              <el-form-item label="节点ID:">
                <el-input v-model="item.id" size="small" />
              </el-form-item>
              <el-form-item label="x坐标：">
                <el-input
                  type="Number"
                  v-model="item.style.x"
                  size="small"
                  placeholder="x"
                />
              </el-form-item>
              <el-form-item label="y坐标：">
                <el-input
                  type="Number"
                  v-model="item.style.y"
                  size="small"
                  placeholder="y"
                />
              </el-form-item>
              <el-form-item label="label:">
                <el-input v-model="item.data.label" size="small" />
              </el-form-item>
              <el-form-item label="category:">
                <el-input v-model="item.data.category" size="small"/>
              </el-form-item>
            </el-form>
          </el-collapse-item>
        </el-collapse>
        <el-form-item label="边配置：">
          <el-button size="small" @click="handAddCollapse">+</el-button>
        </el-form-item>
        <el-collapse>
          <el-collapse-item
            v-for="(item, index) in edgesOptions"
            :key="item.id"
            :name="item.id"
          >
            <template #title>
              <el-icon
                v-if="item.name !== '1'"
                class="header-icon"
                @click.stop="handDelete(index)"
              >
                <CircleClose />
              </el-icon>
              面板{{ item.id }}
            </template>
            <el-form>
              <br />
              <el-form-item label="边ID:">
                <el-input v-model="item.id" size="small" />
              </el-form-item>
              <el-form-item label="来源:">
                <el-input v-model="item.source" size="small" />
              </el-form-item>
              <el-form-item label="目标:">
                <el-input v-model="item.target" size="small" />
              </el-form-item>
            </el-form>
          </el-collapse-item>
        </el-collapse>
      </el-form>
    </CommonAttr>
  </div>
</template>

<script>
import CommonAttr from "@/custom-component/common/CommonAttr.vue";
import { rootStore } from "@/stores/rootStore";
import { isEmpty, getComputedGet, getComputedSet } from "@/utils/utils";

export default {
  components: { CommonAttr },
  computed: {
    curComponent() {
      return rootStore.dataCenter.curComponent;
    },
    nodesOptions: {
      get() {
        return getComputedGet(
          "nodes",
          this.curComponent.dataBinds,
          rootStore.dataConfig.stateSet,
          this.curComponent.propValue
        );
      },
      set(val) {
        getComputedSet(
          "nodes",
          this.curComponent.dataBinds,
          rootStore.dataConfig.stateSet,
          this.curComponent.propValue,
          val
        );
      },
    },
    edgesOptions: {
      get() {
        return getComputedGet(
          "edges",
          this.curComponent.dataBinds,
          rootStore.dataConfig.stateSet,
          this.curComponent.propValue
        );
      },
      set(val) {
        getComputedSet(
          "edges",
          this.curComponent.dataBinds,
          rootStore.dataConfig.stateSet,
          this.curComponent.propValue,
          val
        );
      },
    },
  },
};
</script>
