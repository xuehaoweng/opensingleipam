import { baseURL } from './axios.config'

export const baseAddress = ''

export const test = '/test'

export const login = '/ipam/api-token/'

export const updateUserInfo = '/updateUser'

export const addUserInfo = '/addUser'
export const WebRouter = '/rbac/system/menu/web_router/'
export const getMenuListByRoleId = '/vue3/getMenusByRoleId'
export const getSubnetTree = '/ipam/v1/subnet_tree/'
export const PostAddressHandel = '/ipam/v1/address_handel/'
export const getinterval_schedule = '/ipam/v1/interval_schedule/'
export const getSubnetAddress = '/ipam/v1/subnet/'
export const getUserOplogs = '/ipam/users/oplogs/'
export const getperiodic_taskList = '/ipam/v1/periodic_task/'

export const jobcenterTaskUrl = 'ipam/v1/jobCenter/'







declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $urlPath: Record<string, string>
  }
}
