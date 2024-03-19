import { ref } from 'vue'
import importDataIcon from '../assets/icons/importData.svg'
import exportDataIcon from '../assets/icons/exportData.svg'
import syslabRetreatIcon from '../assets/icons/syslabRetreat.svg'
import syslabForwardIcon from '../assets/icons/syslabForward.svg'
import simulateIcon from '../assets/icons/simulate.svg'
import saveIcon from '../assets/icons/save.svg'
import clearIcon from '../assets/icons/forbidBreakpoint.svg'


export const actions = ref([
  {
    icon: importDataIcon,
    title: '导入',
    key: 'import'
  },
  {
    icon: exportDataIcon,
    title: '导出',
    key: 'export'
  },
  {
    icon: syslabRetreatIcon,
    title: '撤销',
    key: 'canceldo'
  },
  {
    icon: syslabForwardIcon,
    title: '重做',
    key: 'redo'
  },
  {
    icon: simulateIcon,
    title: '预览',
    key: 'preview'
  },
  {
    icon: saveIcon,
    title: '出码',
    key: 'generate'
  },
  {
    icon: clearIcon,
    title: '清空',
    key: 'clear'
  }
])