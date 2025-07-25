export default {
  component: 'ErWindow',
  label: '窗口',
  icon: 'VPanel',
  type: 'errantia',
  propValue: {
    funParam: "",
    curWinData: {},
    winDataList: [],
  },
  style: {
    width: '500',
    height: '400',
    fixedWidth: '100%',
    fixedHeight: '100%',
    backgroundColor: '#f8f9fa',
    borderWidth: 1,
    borderColor: '#ccc',
    borderStyle: 'solid',
  },
  position: 'top',
  actionBinds:{
    onSwitchWin: ''
  },
}