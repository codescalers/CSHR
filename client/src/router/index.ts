import { ApiClientBase } from '@/clients/api/base'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', component: () => import('@/views/LoginView.vue') },
    { path: '/', component: () => import('@/views/CalendarView.vue') },
    { path: '/pending-requests', component: () => import('@/views/PendingRequests.vue') },
    { path: '/notifications', component: () => import('@/views/NotificationsView.vue') },
    { path: '/locations', component: () => import('@/views/OfficesView.vue') },
    { path: '/dashboard', component: () => import('@/views/DashboardView.vue') },
    { path: '/team', component: () => import('@/views/TeamView.vue') },
    { path: '/users', name: 'users', component: () => import('@/views/UsersView.vue') },
    { path: '/profile', name: 'profile', component: () => import('@/views/ProfileView.vue') },
    { path: '/settings', component: () => import('@/views/SettingsView.vue') },
  ]
})

router.beforeEach(async (to, _, next) => {
  const user = ApiClientBase.user

  if (!user.value) {
    return to.path === '/login' ? next() : next('/login')
  }

  if (user.value.fullUser.user_type.toLowerCase() !== 'admin' && to.path === '/dashboard') {
    return next('/')
  }

  next()
})

export default router
