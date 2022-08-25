// 测试用例增删改查接口管理

// 导入已经配置好的 axios 实例
import axios from './http'

const testcase = {
  // 获取用例信息
  getTestcase(params){
    return axios({
      method: "GET",
      url: "/testcase",
      // 如果是传递拼接在 url 中的参数，要使用 params
      params: params
    })
  },
  // 添加用例
  addTestcase(data) {
    return axios({
      method: "POST",
      url: "/testcase",
      // 如果是传递请求体，要使用 data
      data: data
    })
  },
  // 删除用例
  deleteTestcase(data){
    return axios({
      method: "DELETE",
      url: "/testcase",
      data: data
    })
  },
  // 修改用例
  updateTestcase(data) {
    return axios({
      method: "PUT",
      url: "/testcase",
      data: data
    })
  }
}

// 导出
export default testcase