<template>
  <v-card>
    <v-layout>
      <v-navigation-drawer v-if="$route.path != '/login'" theme="dark" permanent>
        <v-img :src="logo" max-width="150" class="ml-3 mt-10 mb-4"></v-img>
        <v-list color="transparent">
          <template v-for="item in filteredItems" :key="item.title">
            <v-list-item
              :prepend-icon="item.icon"
              :class="{ 'router-link-active': $route.path === item.path }"
            >
              <router-link :to="item.path" class="router-link">
                {{ item.title }}
              </router-link>
            </v-list-item>
          </template>
        </v-list>
      </v-navigation-drawer>
      <v-main style="min-height: 100vh">
        <template v-if="isReadyRouter.state.value">
          <CshrToolbar v-if="$route.path != '/login'" @logout="logout" />
          <router-view />
        </template>
        <div class="d-flex justify-center align-center h-100" v-else>
          <VProgressCircular size="80" width="5" indeterminate color="primary" />
        </div>
      </v-main>
    </v-layout>
  </v-card>
</template>

<script lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAsyncState } from '@vueuse/core'
import logo from '@/assets/cshr_logo.png'
import { computed } from 'vue'
import CshrToolbar from './CshrToolbar.vue'
import { $api } from '@/clients'
import { ApiClientBase } from '@/clients/api/base'

export default {
  name: 'SideDrawer',
  components: {
    CshrToolbar
  },
  setup() {
    const $route = useRoute()
    const $router = useRouter()
    const user = ApiClientBase.user

    const isReadyRouter = useAsyncState(async () => {
      await $router.isReady()
      return true
    }, false)

    const navItems = [
      {
        icon: 'mdi-calendar-range',
        title: 'Calendar',
        path: '/'
      },
      {
        icon: 'mdi-bell',
        title: 'Notifications',
        path: '/notifications'
      },
      {
        icon: 'mdi-briefcase',
        title: 'My Team',
        path: '/team'
      },
      {
        icon: 'mdi-account-multiple-outline',
        title: 'Threefold Team',
        path: '/users'
      },
      {
        icon: 'mdi-view-dashboard',
        title: 'Dashboard',
        path: '/dashboard'
      },
      {
        icon: 'mdi-cog',
        title: 'Settings',
        path: '/settings'
      },
      {
        icon: 'mdi-account',
        title: 'Profile',
        path: '/profile'
      }
    ]

    const filteredItems = computed(() =>
      navItems.filter((item: any) => {
        return (
          user.value?.fullUser.user_type.toLowerCase() === 'admin' || item.path !== '/dashboard'
        )
      })
    )

    function logout() {
      $api.auth.logout()
      $router.push('/login')
    }

    return {
      isReadyRouter,
      logo,
      $route,
      navItems,
      filteredItems,
      logout
    }
  }
}
</script>

<style scoped>
.router-link {
  text-decoration: none;
  font-weight: bold;
  color: var(--link-color);
  cursor: pointer;
}
</style>
