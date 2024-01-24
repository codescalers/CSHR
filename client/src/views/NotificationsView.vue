<template>
  <v-container>
    <h1 class="my-6">All Notifications</h1>
    <v-data-table :headers="headers" :loading="loading" :items="notifications">
      <template v-slot:loading>
        <v-skeleton-loader type="table-row@5"></v-skeleton-loader>
      </template>
      <template v-slot:[`item.type`]="{ value }">
        <v-chip :color="getStatusColor(value)">
          {{ value.split('_').join(' ') }}
        </v-chip>
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon class="me-2" @click="selectedNotification = item" icon="mdi-eye" />
        <NotificationDetailsDialog route-query="notification-view" v-model="selectedNotification" />
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import { $api } from '@/clients'
import { onMounted, ref } from 'vue'
import { capitalize } from 'vue'
import { getStatusColor } from '@/utils'
import NotificationDetailsDialog from '@/components/NotificationDetailsDialog.vue'

export default {
  name: 'NotificationsView',
  components: {
    NotificationDetailsDialog
  },
  setup() {
    const headers = [
      { title: 'User', align: 'start', sortable: false, key: 'user.full_name' },
      { title: 'Type', align: 'start', key: 'type' },
      { title: 'Content', align: 'start', key: 'title' },
      { title: 'Created At', align: 'start', key: 'created_at' },
      { title: 'Actions', key: 'actions', align: 'end', sortable: false }
    ] as any[]
    const loading = ref(true)
    const notifications = ref<any[]>()
    const showDialog = ref<{ [key: string]: boolean }>({})
    const selectedNotification = ref<any>()

    onMounted(async () => {
      try {
        notifications.value = await $api.notifications.list()
        loading.value = false
      } catch (error) {
        console.error(error)
      }
    })

    async function readNotification(type: string, id: number) {
      return await $api.notifications.read(type, id)
    }

    return {
      headers,
      loading,
      notifications,
      showDialog,
      selectedNotification,
      getStatusColor,
      readNotification,
      capitalize
    }
  }
}
</script>

<style>
.v-list-item-subtitle {
  margin-bottom: 0.5rem;
}
</style>
