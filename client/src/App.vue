<template>
  <v-app>
    <SideDrawer />
  </v-app>
</template>

<script lang="ts">
import { useNotifier } from 'vue3-notifier'
import { useApi } from '@/hooks'
import SideDrawer from './components/SideDrawer.vue'
import { onMounted } from 'vue'
import { useState } from './store'

export default {
  name: 'App',
  components: {
    SideDrawer
  },
  setup() {
    /* Set Notifier in API */
    const api = useApi()
    const notifier = useNotifier()
    const state = useState()
    api && notifier && api.setNotifier(notifier)

    onMounted(() => {
      state.access_token.value = localStorage.access_token
    })
  }
}
</script>
