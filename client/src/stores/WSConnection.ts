import { defineStore } from 'pinia';
import { ref, type Ref } from 'vue';
import { ApiClientBase } from "@/clients/api/base";
import { useAsyncState } from '@vueuse/core';
import { $api } from '@/clients';
import { useNotificationStore } from './notifications';
import { useNotifier } from 'vue3-notifier';
import type { notificationType, WSErrorType } from '@/types';
import { useHomeEventsStore } from './homeEvents';
import { useApi } from '@/hooks';

// Define the store
export const useWSConnectionStore = defineStore('WSConnectionStore', () => {
  const me = ApiClientBase.user.value?.fullUser;
  const WSConnection = ref<WebSocket | null>(null);

  // Initialize notifier and api inside the store
  const notifier = useNotifier();
  const api = useApi();

  if (api && notifier) {
    notifier.notify;
    api.setNotifier(notifier);
  }

  // Actions
  const connect = (): Ref<WebSocket | null> => {
    if (me) {
      WSConnection.value = new WebSocket(`${window.env.SERVER_DOMAIN_NAME_WS}/${me.id}/?token=Bearer ` + localStorage.getItem("USER_ACCESS_KEY"));
    }
    return WSConnection;
  };

  const reconnect = async (): Promise<Ref<WebSocket | null>> => {
    const user = await useAsyncState(() => $api.myprofile.getUser(), null).execute();
    if (user) {
      WSConnection.value = new WebSocket(`${window.env.SERVER_DOMAIN_NAME_WS}/${user.id}/?token=Bearer ` + localStorage.getItem("USER_ACCESS_KEY"));
    }
    return WSConnection;
  };

  const handleIncomingMessage = (event: MessageEvent) => {
    const notifications = useNotificationStore();
    const data: notificationType | WSErrorType = JSON.parse(event.data as string);

    if ('code' in data && 'message' in data) {
      // Handle error
      const error: WSErrorType = data as WSErrorType;
      console.error('Error received from the WebSocket:', error);
      // const noti = notifier.notify({
      //   title: 'An error received from the WebSocket',
      //   description: error.message,
      //   type: 'error',
      // });

      // setTimeout(() => {
      //   noti?.destroy();
      // }, 4000);
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
        type: 'success',
      });

      setTimeout(() => {
        noti?.destroy();
      }, 4000);
    }
  };

  const WSHandleConnection = () => {
    if (window.connections.ws.value) {
      window.connections.ws.value!.onmessage = (event: MessageEvent) =>
        handleIncomingMessage(event);
      window.connections.ws.value!.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
      window.connections.ws.value!.onclose = (event) => {
        console.log('WebSocket connection closed:', event);
      };
    }
  };

  return {
    connect,
    reconnect,
    WSHandleConnection,
  };
});
