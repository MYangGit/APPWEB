<template>
       <el-dropdown @command="handleCommand">
        <span class="el-dropdown-link">
          编程语言：{{ Language.cunLanguage }}
          <el-icon class="el-icon--right">
            <arrow-down />
          </el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="Javascript" >Javascript</el-dropdown-item>
            <el-dropdown-item command="Julia" >Julia</el-dropdown-item>
            <el-dropdown-item command="Python">Python</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
</template>

<script setup>
import { useProgramLanguage } from '@/hooks/useProgramLanguage';
const Language = useProgramLanguage();
const handleCommand = (command) => {
    Language.setCunLanguage(command);
};
</script>

<style lang="less" scoped>
.el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}
</style>