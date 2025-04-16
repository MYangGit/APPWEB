export default {
    component: 'ErForm',
    label: '表单',
    icon: 'VPanel',
    type: 'errantia',
    propValue: {
        size: 'small',
        labelPosition: 'right',
        formData: [
            {
                name: 'ErFormItem1',
                label: '表单项1',
                type: 'input',
                value: '',
            },
            {
                name: 'ErFormItem2',
                label: '表单项2',
                disabled: true,
                type: 'input',
                value: '',
            },
        ],
        activateText: "",
    },
    style: {
      width: 300,
      height: 400,
      backgroundColor: '#fff',
      display: 'block',
      borderWidth: 0,
      borderColor: '#ffffff',
      borderStyle: 'solid',
      fixedWidth: '',
      fixedHeight: '',
      padding: 0
    },
    childs: [],
    actionBinds: {
        onTable: '',
        change: '',
    },
  }