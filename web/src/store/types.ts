export interface UserState {
  userId: number
  token: string
  roleId: number
  roles: string[] | null
  userName: string
  nickName: string
  avatar: string
}
export interface stateInt {
  data: Object
  webSocket: WebSocket
}
