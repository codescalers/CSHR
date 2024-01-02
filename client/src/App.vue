<template>
  <VApp>
    <RouterView />
  </VApp>
</template>

<script lang="ts">
import { ref } from 'vue'

import { useAsyncState } from '@vueuse/core'
import { useApi } from '@/hooks'

export default {
  name: 'App',
  setup() {
    const api = useApi()
    const loginTask = useAsyncState(
      (email: string, password: string) => api.auth.login({ email, password }),
      null,
      { immediate: false }
    )

    const email = ref('')
    const password = ref('')

    function login() {
      loginTask.execute(import.meta.env.DEV ? 1000 : 0, email.value, password.value)
    }

    return { loginTask, login, email, password }
  }
}
</script>
