import { resolve, panic } from '@/utils'

import { ApiClientBase } from './base'

export class AuthApi extends ApiClientBase {
  protected readonly path = '/auth'

  async signup(credentials: SignupInp) {
    const res = await resolve(this.$http.post<SignupOut>(this.getUrl('/signup'), credentials))
    const [out, err] = res

    if (err) {
      panic(err, ['[Auth] signup failed!', err])
    }

    return out.data
  }

  async login(credentials: LoginInp) {
    const [out, err] = await resolve(this.$http.post<LoginOut>(this.getUrl(`/login`), credentials))

    if (err) {
      panic(err, ['[Auth] login failed!', err])
    }

    ApiClientBase.ACCESS_TOKEN = out.data.results.access_token
    return out.data.results
  }

  async refresh(input: RefreshInp) {
    ApiClientBase.assertToken()

    const res = await resolve(this.$http.post<RefreshOut>(this.getUrl(`/token/refresh`), input))
    const [out, err] = res

    if (err) {
      panic(err, ['[Auth] refresh failed!', err])
    }

    return out.data
  }

  async changePassword(input: ChangePasswordInp) {
    ApiClientBase.assertToken()

    const [, err] = await resolve(this.$http.put(this.getUrl('/change-password'), input))

    if (err) {
      panic(err, ['[Auth] change password failed!', err])
    }
  }

  logout() {
    ApiClientBase.assertToken()
    ApiClientBase.ACCESS_TOKEN = null
  }
}

export interface SignupInp {}

export interface SignupOut {}

export interface LoginInp {
  email: string
  password: string
}

export interface LoginOut {
  message: string
  results: {
    id: number
    full_name: string
    first_name: string
    last_name: string
    email: string
    access_token: string
    refresh_token: string
  }
}

export interface RefreshInp {
  refresh: string
}

export interface RefreshOut {
  access: string
  refresh: string
}

export interface ChangePasswordInp {
  old_password: string
  new_password: string
}
