<template>
  <v-list active-class="v-list-item__overlay">
    <v-list-item
      v-for="item in items"
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

<style>
.v-list-item__overlay{
  background-color: #47a2ff !important;
}
.v-list-item:hover > .v-list-item__overlay{
  background-color: #47a2ff !important;

}
.v-list-item--variant-text .v-list-item__overlay {
  background-color: #47a2ff !important;
}
</style>
