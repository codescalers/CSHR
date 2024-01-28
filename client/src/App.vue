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
import { $api } from './clients'
import { useAsyncState } from '@vueuse/core'

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

    onMounted(async() => {
      const {access_token, refresh_token, user} = state
      access_token.value = localStorage.access_token
      refresh_token.value = localStorage.refresh_token
      user.value = useAsyncState(async() => await $api.myprofile.getUser(), null).state
    })
  }
}
</script>
