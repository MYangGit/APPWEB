export default {
  component: 'VCheckBox',
  label: '多选框',
  propValue: {
    disabled: false,
    value: [],
    label: '字段名',
    options: [
      {
        label: 'Label',
        value: 'value'
      }
    ]
  },
  icon: 'input',
  type: 'common',
  style: {
    width: 200,
    height: 34,
    fontSize: '',
    fixedWidth: '',
    fixedHeight: '',
    fontWeight: 400,
    lineHeight: '',
    letterSpacing: 0,
    textAlign: '',
    color: '',
    backgroundColor: '',
  },
  actionBinds: {
    change: ''
  }
}