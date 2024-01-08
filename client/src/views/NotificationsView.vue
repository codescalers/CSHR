<template>
  <v-container>
    <h1 class="my-6">All Notifications</h1>
    <v-data-table :headers="headers" :loading="loading" :items="notifications">
      <template v-slot:loading>
        <v-skeleton-loader type="table-row@5"></v-skeleton-loader>
      </template>
      <template v-slot:item.type="{ value }">
        <v-chip :color="getColor(value)">
          {{ value.split('_').join(' ') }}
        </v-chip>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon class="me-2" @click="showDialogue = true">
          mdi-eye
        </v-icon>
        <CustomVDialog :routeQuery='(item as any).event_id' :modelValue='showDialogue' />

      </template>
  </v-data-table>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients';
import { onMounted, ref } from 'vue'
import CustomVDialog from "../components/vuetify/CustomVDialog.vue"

export default {
  name: "NotificationsView",
  components: {
    CustomVDialog,
  },
  setup() {
    const headers = [
      { title: 'User', align: 'start', sortable: false, key: 'user.full_name' },
      { title: 'Type', align: 'start', key: 'type' },
      { title: 'Content', align: 'start', key: 'title' },
      { title: 'Created At', align: 'start', key: 'created_at' },
      { title: 'Actions', key: 'actions', align: 'end', sortable: false },
    ]
    const loading = ref(true);
    const notifications = ref();
    const showDialogue = ref(false);

    onMounted(async() => {
      await $api.auth.login({
        email: "admin@gmail.com",
        password: "0000"
      });
      notifications.value = await $api.notifications.list();
      loading.value = false;
    })

    function getColor(type: string) {
      switch (type) {
        case "vacations":
          return "green";
        case "hr_letters":
          return "orange";
        default:
          return "grey";
      }
    }

    async function getNotificationDetails(type: string, id: number) {
      await $api.notifications.getNotificationById(type, id);
    }

    return{
      headers,
      loading,
      notifications,
      getColor,
      getNotificationDetails,
      showDialogue,
    }
  }

}
</script>

