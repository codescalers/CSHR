import { type App, inject } from 'vue'

const $globals = Symbol('key:$globals')

export interface $Globals {
  app: App<Element>
}

export function useGlobals(): $Globals
export function useGlobals(app: App<Element>, globals: $Globals): void
export function useGlobals(app?: App<Element>, globals?: $Globals): any {
  // Provide globals
  if (app && globals) {
    app.config.globalProperties.$globals = globals
    return app.provide($globals, globals)
  }

  // inject Global
  return inject($globals) as $Globals
}
