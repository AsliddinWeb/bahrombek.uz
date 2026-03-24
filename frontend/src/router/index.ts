import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0, behavior: 'smooth' }
  },
  routes: [
    {
      path: '/',
      component: () => import('@/pages/HomePage.vue'),
    },
    {
      path: '/publications',
      component: () => import('@/pages/PublicationsPage.vue'),
    },
    {
      path: '/publications/:id',
      component: () => import('@/pages/PublicationDetailPage.vue'),
    },
    {
      path: '/about',
      component: () => import('@/pages/AboutPage.vue'),
    },
    {
      path: '/admin/login',
      component: () => import('@/pages/admin/AdminLogin.vue'),
    },
    {
      path: '/admin',
      component: () => import('@/pages/admin/AdminLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '',        component: () => import('@/pages/admin/AdminDashboard.vue') },
        { path: 'articles', component: () => import('@/pages/admin/AdminArticles.vue') },
        { path: 'profile',  component: () => import('@/pages/admin/AdminProfile.vue') },
        { path: 'settings', component: () => import('@/pages/admin/AdminSettings.vue') },
      ],
    },
    {
      path: '/:pathMatch(.*)*',
      component: () => import('@/pages/NotFound.vue'),
    },
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth) {
    const auth = useAuthStore()
    if (!auth.isLoggedIn) {
      return { path: '/admin/login', query: { redirect: to.fullPath } }
    }
  }
})

export default router
