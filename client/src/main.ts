import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.min.css'
import 'vue3-notifier/style.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@/App.vue'
import router from '@/router'
import { $vuetify } from '@/plugins'
import { defineGlobals } from '@/config'
import { $notifier } from './plugins/notifier'

declare module 'vue' {
  type GlobalComps = import('./config/types').GlobalComps
  type GlobalProps = import('./config/types').GlobalProps

  interface GlobalComponents extends GlobalComps {}
  interface ComponentCustomProperties extends GlobalProps {}
}

createApp(App)
  .use(createPinia())
  .use(router)
  .use($vuetify)
  .use($notifier)
  .use(defineGlobals())

  .mount('#app')
