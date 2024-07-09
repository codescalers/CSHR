import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { notificationType } from '@/types';

export const useNotificationStore = defineStore('notificationStore', () => {
  const notifications = ref<notificationType[]>([]);

  const addNotification = (newNotification: notificationType) => {
    notifications.value.unshift(newNotification);
  };

  const setNotifications = (newNotifications: notificationType[]) => {
    notifications.value = newNotifications;
  };

  const clearNotifications = () => {
    notifications.value = [];
  };

  return {
    notifications,
    addNotification,
    setNotifications,
    clearNotifications,
  };
});
