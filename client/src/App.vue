<template>
  <v-app>
    <SideDrawer />
  </v-app>
</template>

<script lang="ts">
import { useNotifier } from 'vue3-notifier'
import { useApi } from '@/hooks'
import SideDrawer from './components/SideDrawer.vue'

export default {
  name: 'App',
  components: {
    SideDrawer
  },
  setup() {
    /* Set Notifier in API */
    const api = useApi()
    const notifier = useNotifier()
    api && notifier && api.setNotifier(notifier)
    console.log("nenene");
    
  }
}
</script>
