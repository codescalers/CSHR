import type { Plugin, App } from 'vue'

import { useGlobals } from '@/hooks'
import { GLOBAL_COMPONENT } from './types'

export function defineGlobals(): Plugin {
  return {
    install(app: App<Element>) {
      // define globals
      useGlobals(app, { app })

      // define metaEnv
      app.config.globalProperties.$metaEnv = import.meta.env

      // Define global components
      for (const cmp in GLOBAL_COMPONENT) {
        app.component(cmp, Reflect.get(GLOBAL_COMPONENT, cmp))
      }
    }
  }
}
