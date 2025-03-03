export default {
  component: 'VInput',
  label: '输入框',
  propValue: {
    value: '',
    label: '字段名',
    disabled: false,
    showPassword: false,
  },
  exposeAttr: ['value'],
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
    marginLeft: 0,
  },
  actionBinds: {
    change: '',
    blur: '',
  }
}