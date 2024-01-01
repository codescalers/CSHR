import 'vuetify/styles'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@/App.vue'
import router from '@/router'
import { $vuetify } from '@/plugins'
import { defineGlobals } from '@/config'

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
  .use(defineGlobals())

  .mount('#app')
