import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('@/views/Dashboard.vue'),
    },
    {
      path: '/signals',
      name: 'Signals',
      component: () => import('@/views/Signals.vue'),
    },
    {
      path: '/materials',
      name: 'Materials',
      component: () => import('@/views/Materials.vue'),
    },
    {
      path: '/contents',
      name: 'Contents',
      component: () => import('@/views/Contents.vue'),
    },
    {
      path: '/contents/create',
      name: 'CreateContent',
      component: () => import('@/views/CreateContent.vue'),
    },
    {
      path: '/contents/:id',
      name: 'EditContent',
      component: () => import('@/views/EditContent.vue'),
    },
    {
      path: '/ai',
      name: 'AI',
      component: () => import('@/views/AI.vue'),
    },
  ],
})

export default router
