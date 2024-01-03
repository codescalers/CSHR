<template>
  <SideDrawer />
</template>

<script lang="ts">
import { useNotifier } from 'vue3-notifier'
import { useApi } from '@/hooks'
import SideDrawer from './components/SideDrawer.vue'
import { test_api } from '@/tests'

export default {
  name: 'App',
  components: {
    SideDrawer,
  },
  setup() {
    /* Set Notifier in API */
    const api = useApi()
    const notifier = useNotifier()

    api && notifier && api.setNotifier(notifier)

    /* Don't include this in production! */
    import.meta.env.VITE_DEBUG === 'true' && test_api()
  }
}
</script>
