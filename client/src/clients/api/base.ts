import type { AxiosError, AxiosInstance, AxiosResponse } from 'axios'

import { panic, resolve } from '@/utils'
import type { Api } from '@/types'
import type { NotifierService } from 'vue3-notifier'
import type { ApiClient } from './index'
import { useStorage } from '@vueuse/core'
import { useState } from '@/store'
import { capitalize } from 'vue'

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
    const { access_token, refresh_token } = state
    access_token.value = user.access_token
    refresh_token.value = user.refresh_token
    useStorage('access_token', access_token.value, localStorage, { mergeDefaults: true })
    useStorage('refresh_token', refresh_token.value, localStorage, { mergeDefaults: true })
  }

  protected static refresh() {
    const state = useState()
    const {access_token, refresh_token } = state;
    ApiClientBase.assertUser()
    ApiClientBase.USER = {
      ...ApiClientBase.USER!,
      access_token: access_token.value,
      refresh_token: refresh_token.value
    }
  }

  protected static logout() {
    ApiClientBase.assertUser()
    ApiClientBase.USER = null
  }

  protected static assertUser() {
    const token = localStorage.getItem("access_token")
    if (!ApiClientBase.USER && !token) {
      panic(`Expected to login before using this route.`)
    }
  }

  protected getUrl(route: string = '', query: { [key: string]: any } = {}): string {
    const q = Object.entries(query)
      .map((x) => x.join('='))
      .join('&')
    return this.prePath + this.path + route + '/?' + q
  }

  private static normalizeError(err: AxiosError<any>): string {
    const responseData = err.response?.data;
    const errorMessage = responseData?.message ?? err.message;
  
    const errorDetails = Object.entries(responseData?.error || {})
      .map(([_, value]) => `${value}`)
      .join('. ');
  
    return `${errorMessage}${errorDetails ? `. ${capitalize(errorDetails)}` : ''}`;
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
    const token = localStorage.getItem("access_token")

    if (err && !ApiClientBase.USER && token !== null) {
      const user = await ApiClientBase.$api.myprofile.getUser();
      (ApiClientBase.USER as any) = {...user}
    }

    if (err) {
      ApiClientBase.$notifier?.notify({
        type: 'error',
        description: options.normalizeError?.(err, res) ?? ApiClientBase.normalizeError(err) ?? err
      })

      panic(err)
    }

    if (
      (res.config.method === 'post' || res.config.method === 'put') &&
      typeof res.data === 'object' &&
      'message' in (res.data || {})
    ) {
      ApiClientBase.$notifier?.notify({
        type: 'success',
        description: (res.data as any).message
      })
    }

    return (options.transform?.(res.data, res) ?? res.data) as R
  }
}
