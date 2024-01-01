import type { Plugin, App } from 'vue'

import { $globals, $http } from '@/hooks'
import { createHttp } from '@/plugins'

import { GLOBAL_COMPONENT } from './types'

function defineGlobal<T>(app: App<Element>, key: string, symbol: Symbol, value: T): void {
  app.config.globalProperties[key] = value
  app.provide(symbol, value)
}

export function defineGlobals(): Plugin {
  return {
    install(app: App<Element>) {
      const GLOBAL_PROPS = [
        ['$globals', $globals, { app, env: import.meta.env }],
        ['$http', $http, createHttp()]

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
