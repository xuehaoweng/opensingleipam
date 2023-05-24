import { mapTwoLevelRouter } from '@/utils'
import { createRouter, createWebHashHistory } from 'vue-router'

const Layout = () => import('@/components/Layout.vue')

export const constantRoutes = [
  {
    path: '/login',
    name: 'Login',
    hidden: true,
    component: () => import('@/views/login/index.vue'),
  },
  {
    path: '/',
    redirect: '/ip_manage/ipam',
    hidden: true,
  },
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    meta: {
      noShowTabbar: true,
    },
    children: [
      {
        path: '/redirect/:path(.*)*',
        component: (): any => import('@/views/redirect/index.vue'),
      },
    ],
  },
  {
    path: '/personal',
    name: 'personal',
    component: Layout,
    hidden: true,
    meta: {
      title: '个人中心',
    },
    children: [
      {
        path: '',
        component: () => import('@/views/personal/index.vue'),
        meta: {
          title: '个人中心',
        },
      },
    ],
  },
  // {
  //   path: '/index',
  //   component: Layout,
  //   name: 'Index',
  //   meta: {
  //     title: 'Dashboard',
  //     iconPrefix: 'iconfont',
  //     icon: 'dashboard',
  //   },
  //   children: [
  //     {
  //       path: 'home',
  //       name: 'Home',
  //       component: (): any => import('@/views/ip_manage/ipam.vue'),
  //       meta: {
  //         title: '地址管理',
  //         affix: true,
  //         cacheable: true,
  //         iconPrefix: 'iconfont',
  //         icon: 'search',
  //       },
  //     },
  //     {
  //       path: 'task_list',
  //       name: 'task_list',
  //       component: (): any => import('@/views/task_center/task_list.vue'),
  //       meta: {
  //         title: '任务列表',
  //         affix: true,
  //         cacheable: true,
  //         iconPrefix: 'iconfont',
  //         icon: 'menu',
  //       },
  //     },
  //     {
  //       path: 'oplogs',
  //       name: 'oplogs',
  //       component: (): any => import('@/views/users/oplogs.vue'),
  //       meta: {
  //         title: '操作日志',
  //         affix: true,
  //         cacheable: true,
  //         iconPrefix: 'iconfont',
  //         icon: 'user',
  //       },
  //     },
  //   ],
  // },
  
  {
    path: '/404',
    name: '404',
    hidden: true,
    component: () => import('@/views/exception/404.vue'),
  },
  {
    path: '/500',
    name: '500',
    hidden: true,
    component: () => import('@/views/exception/500.vue'),
  },
  {
    path: '/403',
    name: '403',
    hidden: true,
    component: () => import('@/views/exception/403.vue'),
  },
]
const router = createRouter({
  history: createWebHashHistory(),
  routes: mapTwoLevelRouter(constantRoutes),
})

export default router
