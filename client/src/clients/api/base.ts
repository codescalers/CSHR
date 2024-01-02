import type { AxiosError, AxiosInstance, AxiosResponse } from 'axios'

import { panic, resolve } from '@/utils'
import type { Api } from '@/types'
import type { NotifierService } from 'vue3-notifier'

const URL_REGEX = /\/+/g

export abstract class ApiClientBase {
  private static USER: Api.LoginUser | null = null
  protected static $notifier?: NotifierService

  protected static get user(): Api.LoginUser | null {
    return ApiClientBase.USER
  }

  protected readonly $http: AxiosInstance
  protected abstract readonly path: Api.Path

  constructor(
    options: Api.ClientOptions,
    private readonly prePath = ''
  ) {
    this.$http = options.$http
  }

  protected static login(user: Api.LoginUser) {
    ApiClientBase.USER = user
    /* TODO: sync in session storage */
  }

  protected static refresh(res: Api.Returns.Refresh) {
    ApiClientBase.assertUser()
    console.log('[OLD ACCESS]', ApiClientBase.USER?.access_token)
    console.log('[NEW ACCESS]', res.access)

    ApiClientBase.USER = {
      ...ApiClientBase.USER!,
      access_token: res.access,
      refresh_token: res.refresh
    }
    /* TODO: sync in session storage */
  }

  protected static logout() {
    ApiClientBase.assertUser()
    ApiClientBase.USER = null
    /* TODO: sync in session storage */
  }

  protected static assertUser() {
    if (!ApiClientBase.USER) {
      panic(`Expected to login before using this route.`)
    }
  }

  protected getUrl(route: Api.Path): string {
    const url = this.prePath + this.path + route + '/'
    return url.replace(URL_REGEX, '/')
  }

  private static normalizeError(err: AxiosError<any>) {
    return err.response?.data?.detail ?? err.response?.data?.message ?? err.message
  }

  protected async unwrap<T, R = T>(
    req$: Promise<AxiosResponse<T>>,
    options: Api.UnwrapOptions<T, R> = {}
  ) {
    const [res, err] = await resolve(req$)
    if (err) {
      ApiClientBase.$notifier?.notify({
        type: 'error',
        description: options.normalizeError?.(err, res) ?? ApiClientBase.normalizeError(err) ?? err
      })

      panic(err)
    }

    if (typeof res.data === 'object' && 'message' in (res.data || {})) {
      ApiClientBase.$notifier?.notify({
        type: 'success',
        description: (res.data as any).message
      })
    }

    return (options.transform?.(res.data, res) ?? res.data) as R
  }
}
