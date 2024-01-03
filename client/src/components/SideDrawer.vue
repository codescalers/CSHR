<template>
  <v-card>
    <v-layout>
      <v-navigation-drawer
        theme="dark"
        permanent
      >
        <v-list color="transparent">
          <template v-for='item in navItems' :key='item.title'>
            <v-list-item 
            :prepend-icon="item.icon">
            <router-link :to="item.path" class='router-link' :class="{ 'router-link-active': $route.path === item.path }">
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
      <v-main style="height: 400px"></v-main>
    </v-layout>
  </v-card>
</template>

<script lang="ts">
import { useRoute } from 'vue-router';

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

    return {
      $route,
      navItems,
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
