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
          primary: "#3399CC",
          info: "#d9d9d9",
          warning :"#fb8c00",
          graytitle: "#333",
        
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
