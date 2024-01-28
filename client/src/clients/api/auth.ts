import { ApiClientBase } from './base'

import type { Api } from '@/types'

export class AuthApi extends ApiClientBase {
  protected readonly path = '/auth'

  async login(input: Api.Inputs.Login) {
    const user = await this.unwrap(
      this.$http.post<Api.Returns.Login>(this.getUrl('/login'), input),
      { transform: (d) => d.results }
    )

    ApiClientBase.login(user)

    return user
  }

  register(input: Api.Inputs.Register) {
    ApiClientBase.assertUser()
    return this.unwrap(this.$http.post<Api.Returns.Register>(this.getUrl('/signup'), input), {
      transform: (d) => d.results
    })
  }

  async refresh(input: Api.Inputs.Refresh) {
    ApiClientBase.assertUser()
    const res = await this.unwrap(
      this.$http.post<Api.Returns.Refresh>(this.getUrl('/token/refresh/'), input)
    )

    ApiClientBase.refresh()

    return res
  }

  async changePassword(input: Api.Inputs.ChangePassword) {
    ApiClientBase.assertUser()
    return this.unwrap(this.$http.put(this.getUrl('/change-password'), input))
  }
}
