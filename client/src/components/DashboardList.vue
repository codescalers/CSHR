<template>
  <v-container>
    <v-card variant="outlined" class="pa-2 card-outline">
      <v-list active-class="v-list-item__overlay">
        <v-list-item
          v-for="item in items"
          :key="item.id"
          @click="selectTab(item)"
          :class="{ 'active-item': item.active }"
        >
          <v-list-item-content>
            <v-list-item-title class="font-weight-bold">{{ item.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { DASHBOARD_ITEMS as items } from '@/utils'
import { useRouteQuery } from '@vueuse/router';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: 'DashboardList',
  emits: ['item-selected'],
  setup(_, { emit }) {
    const activeTab = useRouteQuery<undefined | string>('tab', undefined);
    const $route = useRoute();

    const itemsRef = ref(items);

    const resetActiveTab = () => {
      itemsRef.value.forEach(item => item.active = false);
    };

    const selectTab = (item: { id: number; name: string; active: boolean }) => {
      resetActiveTab();
      item.active = true;
      activeTab.value = `${item.id}`;
      emit('item-selected', item);
    };

    onMounted(() => {
      const tabQuery = $route.query['tab'];
      if (tabQuery && !isNaN(+tabQuery)) {
        const item = itemsRef.value.find(i => i.id === +tabQuery);
        if (item) {
          resetActiveTab();
          item.active = true;
          emit('item-selected', item);
        } else {
          activeTab.value = undefined;
        }
      } else {
        resetActiveTab();
        items.value[0].active = true
      }
    });

    return {
      items: itemsRef,
      selectTab
    };
  }
};
</script>

<style>
.v-list-item__overlay {
  background-color: #47a2ff !important;
}
.v-list-item:hover > .v-list-item__overlay {
  background-color: #47a2ff !important;
}
.v-list-item--variant-text .v-list-item__overlay {
  background-color: #47a2ff !important;
}
.active-item {
  background-color: #143453 !important;
}
.card-outline{
  border-color: #67696b !important;
}
</style>
