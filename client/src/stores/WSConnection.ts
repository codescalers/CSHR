import { defineStore } from 'pinia';
import { ref } from 'vue';
import { ApiClientBase } from "@/clients/api/base";

// Define the store
export const useWSConnectionStore = defineStore('WSConnectionStore', () => {
  const me = ApiClientBase.user.value?.fullUser;
  const WSConnection = ref<WebSocket | null>(null);

  // Actions
  const initializeWebSocket = () => {
    if (me) {
      WSConnection.value = new WebSocket(`${window.env.SERVER_DOMAIN_NAME_WS}/${me.id}/?token=Bearer ` + localStorage.getItem("USER_ACCESS_KEY"));
    }
    return WSConnection;
  };

  const getWSConnection = () => {
    return WSConnection
  }

  return {
    initializeWebSocket,
    getWSConnection,
  };
});
