import type { AxiosInstance } from 'axios'
import { inject } from 'vue'

export const $http = Symbol('key:$http')

export function useHttp() {
  return inject($http) as AxiosInstance
}
