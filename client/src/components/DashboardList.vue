<template>
  <v-list>
    <v-list-item
      v-for="item in items"
      active-class="v-list-item__overlay"
      :key="item.id"
      @click="$emit('item-selected', item)"
    >
      <v-list-item-content>
        <v-list-item-title class="font-weight-bold">{{ item.name }}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script lang="ts">
import { DASHBOARD_ITEMS as items } from '@/utils'
export default {
  name: 'DashboardList',
  emits: {
    'item-selected': (item: Object) => item
  },
  setup() {
    return {
      items
    }
  }
}
</script>
