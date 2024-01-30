import type { AxiosError, AxiosInstance, AxiosResponse } from 'axios'

import { isValidToken, panic, resolve } from '@/utils'
import type { Api } from '@/types'
import type { NotifierService } from 'vue3-notifier'
import type { ApiClient } from './index'
// import { useStorage } from '@vueuse/core'
// import { useState } from '@/store'
import { capitalize, ref } from 'vue'
import { useRouter } from 'vue-router'

export abstract class ApiClientBase {
  public static USER_KEY = 'LOGGED_IN_USER'
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

  // protected static $router = useRouter()
  protected static login(user: Api.LoginUser) {
    localStorage.setItem(ApiClientBase.USER_KEY, btoa(JSON.stringify(user)))
    ApiClientBase.USER.value = user
    console.log('login', { user })

    // const state = useState()
    // const { access_token, refresh_token } = state
    // access_token.value = user.access_token
    // refresh_token.value = user.refresh_token
    // useStorage('access_token', access_token.value, localStorage, { mergeDefaults: true })
    // useStorage('refresh_token', refresh_token.value, localStorage, { mergeDefaults: true })
  }

  protected static refresh(res: Api.Returns.Refresh) {
    this.assertUser()
    ApiClientBase.USER.value = {
      ...ApiClientBase.USER.value!,
      access_token: res.access,
      refresh_token: res.refresh
    }
  }

  protected static logout() {
    ApiClientBase.assertUser()
    localStorage.removeItem(ApiClientBase.USER_KEY)
    ApiClientBase.USER.value = null
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

  private static normalizeError(err: AxiosError<any>): string {
    const responseData = err.response?.data
    const errorMessage = responseData?.message ?? err.message

    const errorDetails = Object.entries(responseData?.error || {})
      .map(([_, value]) => `${value}`)
      .join('. ')

    return `${errorMessage}${errorDetails ? `. ${capitalize(errorDetails)}` : ''}`
  }

  protected async unwrap<T, R = T>(
    req$: Promise<AxiosResponse<T>>,
    options: Api.UnwrapOptions<T, R> = {}
  ) {
    const [res, err] = await resolve(req$)

    // TODO: fix refresh token
    // const user = ApiClientBase.USER
    // const access_token = localStorage.getItem('access_token')
    // const refresh_token = localStorage.getItem('refresh_token')
    // if (
    //   user?.access_token &&
    //   user?.refresh_token &&
    //   !isValidToken(access_token) &&
    //   isValidToken(refresh_token)
    // ) {
    //   await ApiClientBase.$api.auth.refresh({ refresh: refresh_token })
    // }

    // check if error indicate the token needs to be refreshed

    if (
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

      // if (err.response.status == 401) {
      //   ApiClientBase.$router.push('/login')
      // }

      panic(err)
    }

    return (options.transform?.(res.data, res) ?? res.data) as R
  }
}
