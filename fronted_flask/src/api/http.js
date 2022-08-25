// 完成 http 请求的基本配置
// 导入 axios
import axios from 'axios'

// 创建 axios 实例
var instance = axios.create({
  // 请求头
  headers: {
    'Content-Type': 'application/json'
  },
  // 超时时间
  timeout: 2500,
  // 基础 url，接口服务地址
  // baseURL: 'http://localhost:5000/'
  baseURL: 'http://127.0.0.1:5000/'
  // baseURL: 'http://39.102.48.202:6099/'
})
axios.interceptors.request.use(
  config => {
    let url = config.url
    // get参数编码
    if (config.method === 'get' && config.params) {
      url += '?'
      let keys = Object.keys(config.params)
      for (let key of keys) {
        url += `${key}=${encodeURIComponent(config.params[key])}&`
      }
      url = url.substring(0, url.length - 1)
      config.params = {}
    }
    config.url = url
    return config
  })

export default instance