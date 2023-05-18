import { createStore } from 'vuex'
import { stateInt } from '../types'

const state: stateInt = {
  //推送消息
  data: {},
  webSocket: null,
}

export default createStore({
  state,
  mutations: {
    //websocket初始化
    initWebsocket(state) {
      state.webSocket = new WebSocket(
        // 此处填写你要连接的ws地址
        'ws://127.0.0.1:3000/ws/test/' + Math.random()
      )
      //建立连接
      state.webSocket.onopen = function () {
        /*
         * 连接成功
         * */
        console.log('通讯开始')
        // 发送心跳防止ws协议自动断联
        setInterval(() => {
          state.webSocket.send('1')
        }, 1000 * 60)
      }
      //接收服务端消息
      state.webSocket.onmessage = function (e) {
        /*
         * 收到消息时回调函数
         * */
        console.log('收到的数据：', e.data)
        // 如果数据对象为字符串，可转换为对象格式
        const data = JSON.parse(e.data)
        state.data = e.data
        console.log(data)
      }
      state.webSocket.onerror = function () {
        /*
         * 通讯异常
         * */
        console.log('通讯异常')
      }
      state.webSocket.close = function () {
        /*
         * 关闭连接时回调函数
         * */
        console.log('连接已断开')
      }
    },
  },
  actions: {},
  modules: {},
})
