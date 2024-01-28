import { createGlobalState } from '@vueuse/core'
import { ref } from 'vue'

export const useState = createGlobalState(() => {
  const access_token = ref('')
  const refresh_token = ref('')
  const user = ref()
  const rememberMe = ref(false)

  return { access_token, refresh_token, user, rememberMe }
})
