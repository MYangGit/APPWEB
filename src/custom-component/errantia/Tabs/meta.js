export default {
  component: 'ErTabs',
  label: '动态标签页',
  icon: 'tabs',
  type: 'errantia',
  propValue: {
    fixed: "",
    activateText: "",
    tabsItem: [
      {
        name: 'ErTabs1',
        label: 'ErTabs1',
        visible: true,
        closable: false,
        disabled: false,
      }
    ]
  },
  style: {
    width: 400,
    height: 200,
    fixedWidth: '',
    fixedHeight: '',
    display: 'block',
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#dcdfe6',
    borderStyle: 'solid',
  },
  position: 'top',
  childs: [],
  items: [],
  actionBinds: {
    onClickTab: '',
  }
}