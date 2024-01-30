import { ApiClientBase } from '@/clients/api/base'
import { isAuthenticated, isAdmin } from '@/hooks'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', component: () => import('@/views/LoginView.vue') },
    { path: '/', component: () => import('@/views/CalendarView.vue') },
    { path: '/notifications', component: () => import('@/views/NotificationsView.vue') },
    { path: '/team', component: () => import('@/views/TeamView.vue') },
    { path: '/users', name: 'users', component: () => import('@/views/UsersView.vue') },
    { path: '/dashboard', component: () => import('@/views/DashboardView.vue') },
    { path: '/settings', component: () => import('@/views/SettingsView.vue') },
    { path: '/profile', name: 'profile', component: () => import('@/views/ProfileView.vue') },
    { path: '/register', component: () => import('@/views/RegisterView.vue') }
  ]
})

router.beforeEach(async (to, _, next) => {
  const isAuth = ApiClientBase.isAuth()

  console.log(to.path, { isAuth })

  if (!isAuth) {
    return to.path === '/login' ? next() : next('/login')
  }

  // if (isAuth) {}

  next()
})

// router.beforeEach(async (to, _, next) => {
//   // If the user is not authenticated and route to login page
//   if (!isAuthenticated.value && to.path !== '/login') {
//     // Redirect the user to the login page
//     next('/login')
//     // if user is not admin hide dashboard and redirect to home
//   } else if (
//     (isAuthenticated.value && to.path === '/login') ||
//     (!isAdmin.value && to.path === '/dashboard')
//   ) {
//     // If authenticated and trying to access the login page, redirect to home
//     next('/')
//   } else {
//     // Continue navigation for other cases
//     next()
//   }
// })

export default router
