import Axios, { AxiosResponse } from 'axios'
import qs from 'qs'
import Cookies from 'js-cookie'

export const baseURL = ''
// mock 接口
// export const baseURL = 'http://localhost:8080/'

export const CONTENT_TYPE = 'Content-Type'

export const FORM_URLENCODED = 'application/x-www-form-urlencoded; charset=UTF-8'

export const APPLICATION_JSON = 'application/json; charset=UTF-8'

export const TEXT_PLAIN = 'text/plain; charset=UTF-8'

// mock 服务封装
const service = Axios.create({
  // baseURL,
  timeout: 10 * 60 * 1000,
  withCredentials: false, // 跨域请求时发送cookie
})
// 在正式发送请求之前进行拦截配置
service.interceptors.request.use(
  (config) => {
    !config.headers && (config.headers = {})
    if (!config.headers.Authorization && Cookies.get('netops-token')) {
      config.headers.Authorization = Cookies.get('netops-token') ? Cookies.get('netops-token') : ''
    }
    if (!config.headers[CONTENT_TYPE]) {
      config.headers[CONTENT_TYPE] = APPLICATION_JSON
    }
    if (config.headers[CONTENT_TYPE] === FORM_URLENCODED) {
      config.data = qs.stringify(config.data)
    }
    return config
  },
  (error) => {
    return Promise.reject(error.response)
  }
)
// 在接口返回数据的时候进行一次拦截
service.interceptors.response.use(
  (response: AxiosResponse): AxiosResponse => {
    // console.log(response)
    if (response.status === 200) {
      return response
    }
    if (response.status === 201) {
      return response
    }
    if (response.status === 204) {
      return response
    } else {
      throw new Error(response.status.toString())
    }
  },
  (error) => {
    if (import.meta.env.MODE === 'development') {
      console.log(error)
    }
    return Promise.reject({ code: 500, msg: '服务器异常，请稍后重试…' })
  }
)

export default service
