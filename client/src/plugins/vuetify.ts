import { createVuetify } from 'vuetify'

import CustomVDialog from '@/components/vuetify/CustomVDialog.vue'

export const $vuetify = createVuetify({
  defaults: {
    /* Add global defaults here */
    VAlert: {
      variant: 'tonal'
    }
  },
  theme: {
    defaultTheme: 'dark',
    themes: {
      dark: {
        dark: true,
        colors: {
        
        }
      },
      light: {
        dark: false,
        colors: {
        
        }
      }
    }
  },
  components: {
    VDialog: CustomVDialog
  }
})
