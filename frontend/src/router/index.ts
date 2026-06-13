import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../components/Layout.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Layout,
      redirect: '/dashboard',
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: () => import('../views/Dashboard.vue'),
          meta: { title: '数据看板' },
        },
        {
          path: 'futures',
          name: 'Futures',
          component: () => import('../views/Futures.vue'),
          meta: { title: '期货行情' },
        },
        {
          path: 'spot',
          name: 'SpotPrice',
          component: () => import('../views/SpotPrice.vue'),
          meta: { title: '现货价格' },
        },
        {
          path: 'fundamentals',
          name: 'Fundamentals',
          component: () => import('../views/Fundamentals.vue'),
          meta: { title: '供需基本面' },
        },
        {
          path: 'news',
          name: 'News',
          component: () => import('../views/News.vue'),
          meta: { title: '新闻资讯' },
        },
        {
          path: 'weather',
          name: 'Weather',
          component: () => import('../views/Weather.vue'),
          meta: { title: '天气数据' },
        },
        {
          path: 'enso',
          name: 'Enso',
          component: () => import('../views/Enso.vue'),
          meta: { title: 'ENSO气候指数' },
        },
      ],
    },
  ],
})

export default router
