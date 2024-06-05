export default {
  component: 'ErAutoDrop',
  label: '标题下拉板',
  icon: 'VPanel',
  type: 'errantia',
  propValue: {
    titleWidth: 300,
    titleHeight: 100,
    disabled: false,
    activate: false,
    activateText: '',
    trigger: 'contextmenu',
    floatHeight: 200,
    floatWidth: 200,
    dropdownMenu: [
      { name: 'Action 1', command: 'a', disabled: false, divided: false},
    ]
  },
  style: {
    width: 300,
    height: 100,
    backgroundColor: '#fff',
    display: 'block',
  },
  childs: [],
  actionBinds: {
    clickCommand: ''
  }
}