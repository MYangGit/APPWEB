export default {
  component: 'ErTable',
  label: '表格',
  propValue: {
    showBorder: false,
    activeClickRow: false,
    showOperate: false,
    serialNumber: false,
    textAlign: 'left',
    columns: [
        {
          title: '姓名',
          key: 'name',
        },
        {
          title: '年龄',
          key: 'age',
        },
        {
          title: '性别',
          key: 'sex',
        },
    ],
    dataSource: [
      {
        name: '小杨',
        age: 18,
        sex: '男'
      },
      {
        name: '小芳',
        age: 18,
        sex: '女'
      }
    ],
  },
  icon: 'table',
  type: 'errantia',
  style: {
    width: 300,
    height: 200,
    fixedWidth: '',
    fixedHeight: '',
    backgroundColor: '#fff',
  },
  actionBinds: {
    onClickRow: '',
    onClickDelete: '',
    onNameBlur:'',
    onDbClickRow:'',
    onContextMenuRow:'',
  }
}