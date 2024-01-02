import type { Plugin, App } from 'vue'

import { $globals_key, $api_key } from '@/hooks'
import { $api } from '@/clients'

import { GLOBAL_COMPONENT } from './types'

function defineGlobal<T>(app: App<Element>, key: string, symbol: Symbol, value: T): void {
  app.config.globalProperties[key] = value
  app.provide(symbol, value)
}

export function defineGlobals(): Plugin {
  return {
    install(app: App<Element>) {
      const GLOBAL_PROPS = [
        ['$globals', $globals_key, { app, env: import.meta.env }],
        ['$api', $api_key, $api]

        // important as const
      ] as const

      // Define global props
      for (const [key, symbol, value] of GLOBAL_PROPS) {
        defineGlobal(app, key, symbol, value)
      }

      // Define global components
      for (const cmp in GLOBAL_COMPONENT) {
        app.component(cmp, Reflect.get(GLOBAL_COMPONENT, cmp))
      }
    }
  }
}
