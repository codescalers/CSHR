import { type App, inject } from 'vue'

export const $globals_key = Symbol('key:$globals')

export interface $Globals {
  app: App<Element>
  env: ImportMetaEnv
}

export function useGlobals() {
  return inject($globals_key) as $Globals
}
