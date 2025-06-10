export default {
  component: 'ErTable',
  label: '表格',
  propValue: {
    noDataHints: false,
    activateText: "",
    overflowWrap: false,
    showBorder: false,
    activeClickRow: false,
    showOperate: false,
    serialNumber: false,
    textAlign: 'left',
    currUuid: '',
    uuIdName: '',
    columns: [
        { 
          type: 'select',
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
    padding: 0
  },
  actionBinds: {
    onClickTable: '',
    onClickRow: '',
    onClickOperate:'',
    onNameBlur:'',
    onDbClickRow:'',
    onContextMenuRow:'',
    onClickCheckbox:''
  }
}