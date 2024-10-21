<template>
  <v-app>
    <SideDrawer />
  </v-app>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue'
import SideDrawer from './components/SideDrawer.vue'
import { useWSConnectionStore } from './stores/WSConnection'

export default defineComponent({
  name: 'App',
  components: {
    SideDrawer
  },
  setup() {
    const WSConnection = useWSConnectionStore()
    const connection = WSConnection.connect()

    onMounted(async () => {
      window.connections = {
        ws: connection
      }
      WSConnection.WSHandleConnection();
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
