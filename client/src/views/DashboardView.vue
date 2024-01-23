<template>
  <v-container>
    <v-row>
      <v-col cols="4">
        <DashboardList @item-selected="onItemSelected" />
      </v-col>
      <v-col cols="8">
        <v-card flat>
          <v-card-title
            >Dashboard of <strong class="text-blue-lighten-1">{{ office }}</strong> office
            admins</v-card-title
          >
          <v-divider class="mx-4 my-1"></v-divider>
          <component :is="selectedForm" />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { computed, onMounted, ref } from 'vue'
import { DASHBOARD_ITEMS as items } from '@/utils'
import DashboardList from '@/components/DashboardList.vue'
import SetVacations from '@/components/SetVacations.vue'
import SetUserVacations from '@/components/SetUserVacations.vue'
import UpdateOfficeVacations from '@/components/UpdateOfficeVacations.vue'
import AddOffice from '@/components/AddOffice.vue'
import AddUser from '@/components/AddUser.vue'
import UpdateUser from '@/components/UpdateUser.vue'
import { useState } from '../store'
import { $api } from '@/clients'

export default {
  name: 'DashboardView',
  components: {
    DashboardList
  },
  setup() {
    const state = useState()
    const officeId = ref()
    const office = ref()
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

    onMounted(async () => {
      try {
        officeId.value = state.user.value.value?.location.id
        office.value = (await $api.office.read(officeId.value)).name
      } catch (error) {
        console.error(error)
      }
    })

    function onItemSelected(item: any) {
      selectedItem.value = item
    }
    return {
      office,
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
