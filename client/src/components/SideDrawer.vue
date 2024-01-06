<template>
  <v-card>
    <v-layout>
      <v-navigation-drawer
        v-if='isAuthorized'
        theme="dark"
        permanent
      >
        <v-img :src="logo" max-width="150" class="ml-3 mt-6"></v-img>
        <v-list color="transparent">
          <template v-for='item in navItems' :key='item.title'>
            <v-list-item 
            :prepend-icon="item.icon" :class="{ 'router-link-active': $route.path === item.path }">
            <router-link  :to="item.path"  class='router-link'>
              {{item.title}}
            </router-link>
          </v-list-item>
        </template>
        </v-list>

        <template v-slot:append>
          <div class="pa-2">
            <v-btn block>
              Logout
            </v-btn>
          </div>
        </template>
      </v-navigation-drawer>
      <v-main style="min-height: 100vh">
        <router-view />
      </v-main>
    </v-layout>
  </v-card>
</template>

<script lang="ts">
import { useRoute } from 'vue-router';
import { computed } from 'vue';
import logo from '../assets/cshr_logo.png'

export default {
  name: 'SideDrawer',
  setup() {
    const $route = useRoute();
    const navItems = [
      {
        icon: "mdi-calendar-range",
        title: "Calendar",
        path: "/",
      },
      {
        icon: "mdi-bell",
        title: "Notifications",
        path: "/notifications",
      },
      {
        icon: "mdi-briefcase",
        title: "My Team",
        path: "/team",
      },
      {
        icon: "mdi-account-multiple-outline",
        title: "Threefold Team",
        path: "/users",
      },
      {
        icon: "mdi-view-dashboard",
        title: "Dashboard",
        path: "/dashboard",
      },
      {
        icon: "mdi-cog",
        title: "Settings",
        path: "/settings",
      }, 
    ]
    const isAuthorized = computed(() => {
      return localStorage.user ? true : false;
    });

    return {
      logo,
      $route,
      navItems,
      isAuthorized,
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
