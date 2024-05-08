import { inject } from 'vue'
import type { ApiClient } from '@/clients/api'

export const $api_key = Symbol('key:$api')

export function useApi() {
  return inject($api_key) as ApiClient
}
