import { useState } from '@/store'
import { type App, inject, computed } from 'vue'

export const $globals_key = Symbol('key:$globals')
const state = useState()

export const isAuthenticated = computed(() => {
  return state.access_token.value ? true : false
})

export const isAdmin = computed(() => {
  return state.user.value?.value && state.user.value.value.user_type === 'Admin' ? true : false
})

export interface $Globals {
  app: App<Element>
  env: ImportMetaEnv
}

export function useGlobals() {
  return inject($globals_key) as $Globals
}
