<template>
  <v-app>
    <SideDrawer />
  </v-app>
</template>

<script lang="ts">
import { useNotifier } from 'vue3-notifier'
import { useApi } from '@/hooks'
import SideDrawer from './components/SideDrawer.vue'
import { test_api } from '@/tests'
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

    /* Don't include this in production! */
    import.meta.env.VITE_DEBUG === 'true' && test_api()

    onMounted(async() => {
      state.access_token.value = localStorage.access_token
      state.user.value = useAsyncState(async() => await $api.myprofile.getUser(), null).state
    })
  }
}
</script>
