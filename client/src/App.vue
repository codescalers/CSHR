<template>
  <VApp>
    <RouterView />
  </VApp>
</template>

<script lang="ts">
import { useNotifier } from 'vue3-notifier'
import { useApi } from '@/hooks'

export default {
  name: 'App',
  setup() {
    /* Set Notifier in API */
    const api = useApi()
    const notifier = useNotifier()

    api && notifier && api.setNotifier(notifier)
  }
}
</script>
