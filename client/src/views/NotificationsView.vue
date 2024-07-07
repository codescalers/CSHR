<template>
  <v-container class="pa-6 mx-auto">
    <div class="my-6">
      <h2 class="font-weight-medium my-3">All Notifications</h2>
      <v-divider></v-divider>
    </div>
    <v-crad>
      <v-row class="mb-2">
        <v-col class="d-flex justify-end">
          <v-btn
            :disabled="!notifications.length || !hasReadNotifications"
            type="info"
            color="success"
            variant="tonal"
            class="mr-2"
            @click="readAllNotifications"
          >
            <v-icon>mdi-read</v-icon>
            Mark all as read
          </v-btn>
          <v-btn
            :disabled="!notifications.length"
            type="info"
            color="error"
            variant="outlined"
            @click="deleteAllNotifications"
          >
            <v-icon>mdi-trash-can</v-icon>
            Delete all notifications
          </v-btn>
        </v-col>
      </v-row>
      <v-divider></v-divider>
    </v-crad>
    <v-data-table :headers="headers" :loading="loading" :items="notifications">
      <template v-slot:loading>
        <v-skeleton-loader type="table-row@5"></v-skeleton-loader>
      </template>
      <template v-slot:[`item.is_read`]="{ value }">
        <v-icon
          class="me-2"
          :icon="value ? 'mdi-checkbox-multiple-marked-circle-outline' : 'mdi-clock-outline'"
          :color="value ? 'primary' : 'warning'"
        />
      </template>
      <template v-slot:[`item.request.type`]="{ value }">
        <v-chip :color="getStatusColor(value)">
          {{ value.split('_').join(' ') }}
        </v-chip>
      </template>
      <template v-slot:[`item.request.status`]="{ value }">
        <v-chip :color="getStatusColor(value)">
          {{ value.split('_').join(' ') }}
        </v-chip>
      </template>
      <template v-slot:[`item.created_at`]="{ value }">
        {{ formatedDate(value) }}
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon class="me-2" @click="setNotification(item)" icon="mdi-eye" />
      </template>
    </v-data-table>
  </v-container>

  <NotificationDetailsDialog
    route-query="notification-view"
    v-model="selectedNotification"
    @update:approve="handleApprove"
    @update:reject="handleReject"
    @set:notification="setNotification"
  />
</template>

<script lang="ts">
import { $api } from '@/clients'
import { computed, onMounted, ref } from 'vue'
import { capitalize } from 'vue'
import { formatDate, getStatusColor } from '@/utils'
import NotificationDetailsDialog from '@/components/NotificationDetailsDialog.vue'
import { useNotificationStore } from '@/stores/notifications'
import { ApiClientBase } from '@/clients/api/base'
import type { notificationType } from '@/types'

export default {
  name: 'NotificationsView',
  components: {
    NotificationDetailsDialog
  },
  setup() {
    const notificationStore = useNotificationStore()
    const notifications = computed(() => {
      return notificationStore.notifications
    })

    function formatedDate(date: string) {
      const _date = new Date(date)
      const _formatDate = formatDate(date)
      const time = _date.toLocaleTimeString()
      return `${_formatDate} - ${time}`
    }

    const headers = [
      { title: 'Seen', align: 'start', sortable: false, key: 'is_read' },
      { title: 'User', align: 'start', sortable: false, key: 'request.applying_user.full_name' },
      { title: 'Type', align: 'start', key: 'request.type' },
      { title: 'Content', align: 'start', key: 'title' },
      { title: 'Created At', align: 'start', key: 'created_at' },
      { title: 'Status', align: 'start', key: 'request.status' },
      { title: 'Actions', key: 'actions', align: 'end', sortable: false }
    ] as any[]

    const loading = ref(true)
    const showDialog = ref<{ [key: string]: boolean }>({})
    const selectedNotification = ref<any>()

    onMounted(async () => {
      try {
        const notifications = await $api.notifications.list()
        notificationStore.setNotifications(notifications)
        loading.value = false
      } catch (error) {
        console.error(error)
      }
    })

    async function readNotification(type: string, id: number) {
      return await $api.notifications.getNotification(id)
    }

    const hasReadNotifications = computed(() => {
      return notificationStore.notifications.some((notification) => !notification.is_read)
    })

    const setNotification = async (notification: notificationType) => {
      selectedNotification.value = notification
      if (!selectedNotification.value.is_read) {
        selectedNotification.value.is_read = true
        await $api.notifications.readNotification(
          selectedNotification.value.id,
          selectedNotification.value.is_read
        )
      }
    }

    async function readAllNotifications() {
      const me = ApiClientBase.user.value?.fullUser
      if (me) {
        loading.value = true
        const notifications = await $api.notifications.readAllNotifications(me.id)
        notificationStore.setNotifications(notifications)
        loading.value = false
      }
    }

    async function deleteAllNotifications() {
      const me = ApiClientBase.user.value?.fullUser
      if (me) {
        loading.value = true
        await $api.notifications.deleteAllNotifications(me.id)
        notificationStore.setNotifications([])
        loading.value = false
      }
    }

    const handleApprove = (value: string) => {
      const notification = notificationStore.notifications.find(
        (notification) => notification.id === selectedNotification.value?.id
      )
      if (notification) {
        notification.request.status = value
        window.connections.ws.value!.send(
          JSON.stringify({
            event: 'approve_request',
            request_id: notification.request.id
          })
        )
      }
    }

    const handleReject = (value: string) => {
      const notification = notificationStore.notifications.find(
        (notification) => notification.id === selectedNotification.value?.id
      )
      if (notification) {
        notification.request.status = value
        window.connections.ws.value!.send(
          JSON.stringify({
            event: 'reject_request',
            request_id: notification.request.id
          })
        )
      }
    }


    return {
      headers,
      loading,
      notifications,
      showDialog,
      selectedNotification,
      hasReadNotifications,
      getStatusColor,
      readNotification,
      capitalize,
      formatedDate,
      readAllNotifications,
      deleteAllNotifications,

      setNotification,
      handleApprove,
      handleReject,
    }
  }
}
</script>

<style>
.v-list-item-subtitle {
  margin-bottom: 0.5rem;
}
.is-not-read {
  padding: 5px;
  content: '';
  display: inline-block;
  background-color: rgb(42, 165, 93);
  border-radius: 50%;
}
</style>
