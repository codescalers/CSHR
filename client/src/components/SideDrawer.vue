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
      <v-main style="min-height: 100vh" v-if="isReadyRouter.state.value">
        <CshrToolbar v-if="$route.path != '/login'" @logout="logout" />
        <router-view />
      </v-main>
    </v-layout>
  </v-card>
</template>

<script lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAsyncState } from '@vueuse/core'
import logo from '@/assets/cshr_logo.png'
import { useState } from '@/store'
import { isAdmin } from '@/hooks'
import { computed } from 'vue'
import CshrToolbar from './CshrToolbar.vue'

export default {
  name: 'SideDrawer',
  components: {
    CshrToolbar
  },
  setup() {
    const $route = useRoute()
    const $router = useRouter()
    const state = useState()

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
        // Include all items except for 'Dashboard' when isAdmin is false
        return isAdmin.value || item.path !== '/dashboard'
      })
    )

    function logout() {
      if (state.rememberMe.value === false) {
        state.access_token.value = ''
        localStorage.clear()
      }

      $router.push('/login')
    }

    return {
      isReadyRouter,
      logo,
      $route,
      navItems,
      isAdmin,
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
