import { createVuetify } from 'vuetify'

import CustomVDialog from '@/components/vuetify/CustomVDialog.vue'

export const $vuetify = createVuetify({
  defaults: {
    /* Add global defaults here */
  },
  theme: {
    defaultTheme: 'dark'
  },
  components: {
    VDialog: CustomVDialog
  }
})
