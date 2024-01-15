<template>
  <v-container>
    <v-row>
      <v-col cols="4">
        <DashboardList @item-selected="onItemSelected" />
      </v-col>
      <v-col cols="8">
        <component :is="selectedForm" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { computed, ref } from 'vue'
import { DASHBOARD_ITEMS as items } from '@/utils'
import DashboardList from '@/components/DashboardList.vue'
import SetVacations from '@/components/SetVacations.vue'
import SetUserVacations from '@/components/SetUserVacations.vue'
import UpdateOfficeVacations from '@/components/UpdateOfficeVacations.vue'
import AddOffice from '@/components/AddOffice.vue'
import AddUser from '@/components/AddUser.vue'
import UpdateUser from '@/components/UpdateUser.vue'

export default {
  name: 'DashboardView',
  components: {
    DashboardList
  },
  setup() {
    const selectedItem = ref(items[0])
    const selectedForm = computed(() => {
      switch (selectedItem.value.id) {
        case 2:
          return SetUserVacations
        case 3:
          return UpdateOfficeVacations
        case 4:
          return AddOffice
        case 5:
          return AddUser
        case 6:
          return UpdateUser
        default:
          return SetVacations
      }
    })

    function onItemSelected(item: any) {
      selectedItem.value = item
    }
    return {
      DashboardList,
      SetVacations,
      UpdateOfficeVacations,
      SetUserVacations,
      AddOffice,
      AddUser,
      UpdateUser,
      selectedItem,
      selectedForm,
      onItemSelected
    }
  }
}
</script>
