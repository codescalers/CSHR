import { useNotifierPlugin } from 'vue3-notifier'
import { $vuetify } from './vuetify'

import CustomNotification from '@/components/notifier/CustomNotification.vue'

export const $notifier = useNotifierPlugin({
  debug: import.meta.env.DEV,
  timeout: 5_000,
  maxNotifictions: 6,
  plugins: [$vuetify],
  component: CustomNotification
})
