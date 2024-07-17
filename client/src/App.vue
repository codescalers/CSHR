<template>
  <v-app>
    <SideDrawer />
  </v-app>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue'
import { useNotifier } from 'vue3-notifier'
import { useApi } from '@/hooks'
import SideDrawer from './components/SideDrawer.vue'
import { useWSConnectionStore } from './stores/WSConnection'
import { useNotificationStore } from './stores/notifications'
import type { Api, notificationType, WSErrorType } from './types'
import { useHomeEventsStore } from './stores/homeEvents'
import { normalizeVacation } from './utils'

export default defineComponent({
  name: 'App',
  components: {
    SideDrawer
  },
  setup() {
    const api = useApi()
    const notifier = useNotifier()

    if (api && notifier) {
      notifier.notify
      api.setNotifier(notifier)
    }

    const WSConnection = useWSConnectionStore()
    const notifications = useNotificationStore()
    const connection = WSConnection.connect()

    const handleIncomingMessage = (event: MessageEvent) => {
  const data: notificationType | WSErrorType = JSON.parse(event.data as string);

  if ('code' in data && 'message' in data) {
    // Handle error
    const error: WSErrorType = data as WSErrorType;
    const noti = notifier.notify({
      title: 'An error received from the WebSocket',
      description: error.message,
      type: 'error'
    });

    setTimeout(() => {
      noti?.destroy();
    }, 4000);
  } else {
    // Handle notification
    const notification: notificationType = data as notificationType;
    const homeEventsStore = useHomeEventsStore();
    notifications.addNotification(notification);

    if (notification.request.type === "vacation") {
      homeEventsStore.reload = true;
    }

    const noti = notifier.notify({
      title: notification.title,
      description: notification.body,
      type: 'success'
    });

    setTimeout(() => {
      noti?.destroy();
    }, 4000);
  }
};

  onMounted(async () => {
    window.connections = {
      ws: connection
    }

    if (window.connections.ws.value) {
      window.connections.ws.value!.onmessage = (event: MessageEvent) =>
        handleIncomingMessage(event)
      window.connections.ws.value!.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
      window.connections.ws.value!.onclose = (event) => {
        console.log('WebSocket connection closed:', event)
      }
    }
  })
}
})
</script>
<style>
.vue3-notifier-container .text-error {
  background-color: rgb(44, 16, 16) !important;
}
.vue3-notifier-container .text-success {
  background-color: rgb(2, 29, 3) !important;
}
</style>
