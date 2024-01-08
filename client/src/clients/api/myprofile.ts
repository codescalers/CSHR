import { ApiClientBase } from './base'
import type { Api } from '@/types'

export class MyprofileApi extends ApiClientBase {
  protected readonly path = '/myprofile'

  async getUser(query?: Api.Inputs.List) {
    ApiClientBase.assertUser()

    const user = await this.unwrap(
      this.$http.get<Api.Returns.Profile>(this.getUrl('', query)),
      { transform: (d) => d.results }
    )

    return user
  }


  async list() {}

  async update(id: number) {}
}
