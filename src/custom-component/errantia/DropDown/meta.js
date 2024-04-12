export default {
  component: 'ErDropDown',
  label: '下拉面板',
  icon: 'VPanel',
  type: 'errantia',
  propValue: {
    title: '标题',
    titleWidth: 100,
    disabled: false,
    iconPath: 'https://img.icons8.com/ios/452/plus-math.png',
    trigger: 'click',
    floatHeight: 200,
    floatWidth: 200,
    horizontal: true,
    hasSubscript: true,
    marginLeft: 0,
  },
  style: {
    width: 100,
    height: 70,
    backgroundColor: '#fff',
    display: 'block',
    borderWidth: 0,
    borderColor: '#ffffff',
    borderStyle: 'solid',
  },
  childs: [],
  position: 'top',
  actionBinds: {
    click: ''
  }
}