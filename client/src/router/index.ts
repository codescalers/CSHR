import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: () => import('@/views/CalendarView.vue') },
    { path: '/notifications', component: () => import('@/views/NotificationsView.vue') },
    { path: '/team', component: () => import('@/views/TeamView.vue') },
    { path: '/users', component: () => import('@/views/UsersView.vue') },
    { path: '/dashboard', component: () => import('@/views/DashboardView.vue') },
    { path: '/settings', component: () => import('@/views/SettingsView.vue') },
    { path: '/profile', name:"profile", component: () => import('@/views/ProfileView.vue') },
    { path: '/login', component: () => import('@/views/LoginView.vue') },
    { path: '/register', component: () => import('@/views/RegisterView.vue') },
  ]
})

export default router
