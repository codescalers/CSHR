import type { AxiosInstance } from 'axios'

import { panic } from '@/utils'
import type { Api } from '@/types'

const URL_REGEX = /\/+/g

export abstract class ApiClientBase {
  static ACCESS_TOKEN: string | null = null

  protected readonly $http: AxiosInstance
  protected abstract readonly path: Api.Path

  constructor(
    options: Api.ClientOptions,
    private readonly prePath = ''
  ) {
    this.$http = options.$http
  }

  protected static assertToken() {
    if (!ApiClientBase.ACCESS_TOKEN) {
      panic(`Expected to login before using this route.`)
    }
  }

  protected getUrl(route: Api.Path): string {
    const url = this.prePath + this.path + route + '/'
    return url.replace(URL_REGEX, '/')
  }
}
