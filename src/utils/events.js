import { ElMessage } from 'element-plus'
// 编辑器自定义事件
const events = {
    redirect(url) {
        if (url) {
            window.location.href = url.param
        }
    },

    message(msg) {
        if (msg) {
            ElMessage.info(msg.param)
        }
    },

    js(content) {
        if (content) {
            // eslint-disable-next-line no-eval
            eval(content.param)
        }
    },
}

const mixins = {
    methods: events,
}

const eventList = [
    {
        key: 'redirect',
        label: '跳转事件',
        event: events.redirect,
        param: '',
    },
    {
        key: 'message',
        label: 'Message事件',
        event: events.message,
        param: '',
    },
    {
        key: 'js',
        label: '自定义JS事件',
        event: events.js,
        param: '',
    },
]

export { mixins, events, eventList }
