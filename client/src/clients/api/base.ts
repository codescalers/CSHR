import type { AxiosInstance } from 'axios'

import { panic } from '@/utils'

export interface ApiClientOptions {
  $http: AxiosInstance
}

export type UrlPath = `/${string}`

const URL_REGEX = /\/+/g

export abstract class ApiClientBase {
  static ACCESS_TOKEN: string | null = null

  protected readonly $http: AxiosInstance
  protected abstract readonly path: UrlPath

  constructor(options: ApiClientOptions) {
    this.$http = options.$http
  }

  protected static assertToken() {
    if (!ApiClientBase.ACCESS_TOKEN) {
      panic(`Expected to login before using this route.`)
    }
  }

  protected getUrl(route: UrlPath): string {
    const url = this.path + route + '/'
    return url.replace(URL_REGEX, '/')
  }
}
