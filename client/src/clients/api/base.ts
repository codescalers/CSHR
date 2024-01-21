import type { AxiosError, AxiosInstance, AxiosResponse } from 'axios'

import { panic, resolve } from '@/utils'
import type { Api } from '@/types'
import type { NotifierService } from 'vue3-notifier'
import type { ApiClient } from './index'
import { useStorage } from '@vueuse/core'
import { useState } from '@/store'

export abstract class ApiClientBase {
  public static $api: ApiClient
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
    const state = useState()
    const { access_token } = state
    access_token.value = user.access_token
    useStorage('access_token', access_token.value, localStorage, { mergeDefaults: true })
  }

  protected static refresh(res: Api.Returns.Refresh) {
    ApiClientBase.assertUser()
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

  protected getUrl(route: string = '', query: { [key: string]: any } = {}): string {
    const q = Object.entries(query)
      .map((x) => x.join('='))
      .join('&')
    return this.prePath + this.path + route + '/?' + q
  }

  private static normalizeError(err: AxiosError<any>) {
    return err.response?.data?.detail ?? err.response?.data?.message ?? err.message
  }

  protected async unwrap<T, R = T>(
    req$: Promise<AxiosResponse<T>>,
    options: Api.UnwrapOptions<T, R> = {}
  ) {
    const [res, err] = await resolve(req$)
    // check if error indicate the token needs to be refreshed
    if (
      err &&
      err.response.status == 401 &&
      err.response.data.code == 'token_not_valid' &&
      ApiClientBase.USER
    ) {
      await ApiClientBase.$api.auth.refresh({ refresh: ApiClientBase.USER.refresh_token })
    }

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
