import type { AxiosError, AxiosInstance, AxiosResponse } from 'axios'

import { isValidToken, panic, resolve } from '@/utils'
import type { Api } from '@/types'
import type { NotifierService } from 'vue3-notifier'
import type { ApiClient } from './index'
import { ref } from 'vue'
import router from '@/router'

export abstract class ApiClientBase {
  public static USER_KEY = 'LOGGED_IN_USER'
  public static USER_ACCESS_KEY = 'USER_ACCESS_KEY'
  public static $api: ApiClient
  private static readonly USER = ref<Api.LoginUser | null>(null)
  protected static $notifier?: NotifierService

  public static get user() {
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
    localStorage.setItem(ApiClientBase.USER_KEY, btoa(JSON.stringify(user)))
    ApiClientBase.USER.value = user
  }

  protected static refresh(res: Api.Returns.Refresh) {
    this.assertUser()
    ApiClientBase.login({
      ...ApiClientBase.USER.value!,
      access_token: res.access,
      refresh_token: res.refresh
    })
  }

  protected static logout() {
    ApiClientBase.assertUser()
    localStorage.removeItem(ApiClientBase.USER_KEY)
    localStorage.removeItem(ApiClientBase.USER_ACCESS_KEY)
    ApiClientBase.USER.value = null
  }

  protected static assertUser() {
    if (!ApiClientBase.USER.value) {
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
    return (
      err.response?.data?.error?.message ||
      err.response?.data?.detail ||
      err.response?.data.message ||
      err.message
    )
  }

  protected async unwrap<T, R = T>(
    req$: () => Promise<AxiosResponse<T>>,
    options: Api.UnwrapOptions<T, R> = {}
  ) {
    const user = ApiClientBase.user.value
    if (user && !isValidToken(user.access_token)) {
      await resolve(ApiClientBase.$api.auth.refresh({ refresh: user.refresh_token }))
    }

    const req = await resolve(req$())
    let res = req[0]
    let err = req[1]

    const { status, data = {} } = err?.response || {}

    if (status === 401 && data.code === 'token_not_valid' && user) {
      const [data, err2] = await resolve(
        ApiClientBase.$api.auth.refresh({ refresh: user.refresh_token })
      )

      if (data === true && !err2) {
        const req = await resolve(req$())
        res = req[0]
        err = req[1]
      } else {
        if(!router.currentRoute.value.fullPath.includes('login')){
          router.push("/login")
        }
    }

    if (
      res &&
      (res.config.method === 'post' || res.config.method === 'put') &&
      typeof res.data === 'object' &&
      'message' in (res.data || {}) &&
      options.disableNotify !== true
    ) {
      ApiClientBase.$notifier?.notify({
        type: 'success',
        description: (res.data as any).message
      })
    }

    if (err) {
      ApiClientBase.$notifier?.notify({
        type: 'error',
        description: options.normalizeError?.(err, res) ?? ApiClientBase.normalizeError(err) ?? err
      })

      panic(err)
    }

    return (options.transform?.(res.data, res) ?? res.data) as R
  }
}
}