export default {
  component: 'VInputNumber',
  label: '数字输入框',
  propValue: {
    value: 1,
  },
  coreKey: "value",
  icon: 'input',
  type: 'common',
  style: {
    width: 200,
    height: 34,
    fontSize: '',
    fontWeight: 400,
    lineHeight: '',
    letterSpacing: 0,
    textAlign: '',
    color: '',
    backgroundColor: '',
    marginLeft: 0,
  },
  eventOptions: [{ label: '数据改变', value: 'updateValue' }],
  actionBinds: {
    change: ''
  }
}