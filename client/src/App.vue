<template>
  <VApp>
    <RouterView />
  </VApp>
</template>

<script lang="ts">
import { onMounted } from 'vue'

import { useNotifier } from 'vue3-notifier'
import { useApi } from '@/hooks'

import { test_api } from '@/tests'

export default {
  name: 'App',
  setup() {
    /* Set Notifier in API */
    const api = useApi()
    const notifier = useNotifier()

    api && notifier && api.setNotifier(notifier)

    onMounted(() => {
      test_api()
    })
  }
}
</script>
