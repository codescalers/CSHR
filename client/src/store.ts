import { createGlobalState } from '@vueuse/core'
import { ref } from 'vue'

export const useState = createGlobalState(() => {
  const access_token = ref('')
  const user = ref();
  return { access_token, user }
})
