import router, { constantRoutes } from '../router'
// import Cookies from 'js-cookie'
import { get } from '@/api/http'
// getMenuListByRoleId
import { baseAddress, WebRouter } from '@/api/url'
import { RouteRecordRaw } from 'vue-router'
import { isExternal, mapTwoLevelRouter, toHump } from '.'
import { Layout } from '@/components'
import layoutStore from '@/store'
import { defineAsyncComponent } from 'vue'
import LoadingComponent from '../components/loading/index.vue'
import defaultRouteJson from '../../default_menu.json'
// ADMIN_WORK_USER_INFO_KEY, ADMIN_WORK_BUTTON_AUTH,
import { ADMIN_WORK_S_TENANT } from '@/store/keys'
const navigateID = localStorage.getItem(ADMIN_WORK_S_TENANT)
interface OriginRoute {
  name: unknown
  web_path: any
  link_path: any
  menuUrl: string
  menuName?: string
  hidden?: boolean
  outLink?: string
  affix?: boolean
  cacheable?: boolean
  iconPrefix?: string
  icon?: string
  badge?: string | number
  children: Array<OriginRoute>
}

type RouteRecordRawWithHidden = RouteRecordRaw & { hidden: boolean }

function loadComponents() {
  return import.meta.glob('../views/**/*.vue')
}

const asynComponents = loadComponents()

function getRoutes() {
  // console.log(import.meta.env.VITE_LOCAL_ROUTER)
  if (!import.meta.env.VITE_LOCAL_ROUTER) {
    return get({
      url: baseAddress + WebRouter,
      method: 'GET',
      data: { parent__isnull: true, navigate__id: navigateID },
    }).then((res: any) => {
      return generatorRoutes(res.results)
    })
  } else {
    return generatorRoutes(defaultRouteJson.menu)
  }
}

function getComponent(it: OriginRoute) {
  return defineAsyncComponent({
    loader: asynComponents['../views' + it.web_path + '.vue'],
    loadingComponent: LoadingComponent,
  })
}

function getCharCount(str: string, char: string) {
  // //console.log(str)
  const regex = new RegExp(char, 'g')
  const result = str.match(regex)
  const count = !result ? 0 : result.length
  return count
}

function isMenu(path: string) {
  return getCharCount(path, '/') === 1
}

function getNameByUrl(path: string) {
  const temp = path.split('/')
  return toHump(temp[temp.length - 1])
}

function generatorRoutes(res: Array<OriginRoute>) {
  const tempRoutes: Array<RouteRecordRawWithHidden> = []
  res.forEach((it) => {
    const path = it.link_path && isExternal(it.link_path) ? it.link_path : it.web_path
    // //console.log(it)
    const route: RouteRecordRawWithHidden = {
      path: path,
      name: getNameByUrl(path),
      hidden: !!it.hidden,
      component: it.web_path && isMenu(it.web_path) ? Layout : getComponent(it),

      meta: {
        title: it.name,
        affix: !!it.affix,
        cacheable: !!it.cacheable,
        icon: it.icon || 'menu',
        iconPrefix: it.iconPrefix || 'iconfont',
      },
    }
    if (it.children) {
      route.children = generatorRoutes(it.children)
    }
    tempRoutes.push(route)
  })
  return tempRoutes
}

const whiteRoutes: string[] = ['/login', '/404', '/403', '/500']

// function isTokenExpired(): boolean {
//   const token = Cookies.get('netops-token')
//   return !!token
// }
router.beforeEach(async (to) => {
  // console.log('import.meta.env.VITE_LOCAL_ROUTER',import.meta.env.VITE_LOCAL_ROUTER)
  if (whiteRoutes.includes(to.path)) {
    return true
  } else {
    const isEmptyRoute = layoutStore.isEmptyPermissionRoute()
    // console.log(isEmptyRoute)
    if (isEmptyRoute) {
      const accessRoutes: Array<RouteRecordRaw> = []
      let webRoutes: any = []

      if (!import.meta.env.VITE_LOCAL_ROUTER) {
        webRoutes = await getRoutes()
      } else {
        // //console.log(defaultRouteJson.menu)
        // 本地 rundev加载
        webRoutes = generatorRoutes(defaultRouteJson.menu)
        //console.log('webRoutes', webRoutes)
      }

      // const tempRoutes = await getRoutes()
      accessRoutes.push(...webRoutes)
      const mapRoutes = mapTwoLevelRouter(accessRoutes)
      mapRoutes.forEach((it: any) => {
        router.addRoute(it)
      })
      router.addRoute({
        path: '/:pathMatch(.*)*',
        redirect: '/404',
        hidden: true,
      } as RouteRecordRaw)
      layoutStore.initPermissionRoute([...constantRoutes, ...accessRoutes])
      return { ...to, replace: true }
    } else {
      return true
    }
    // }
  }
})
