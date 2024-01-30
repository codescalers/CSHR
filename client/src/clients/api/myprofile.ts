import { ApiClientBase } from './base'
import type { Api } from '@/types'

export class MyprofileApi extends ApiClientBase {
  protected readonly path = '/myprofile'

  getUser(query?: Api.Inputs.List) {
    ApiClientBase.assertUser()

    return this.unwrap(this.$http.get<Api.Returns.Profile>(this.getUrl('', query)), {
      transform: (d) => d.results
    })
  }

  async list() {}

  async update(id: number, input: Api.Inputs.UsersAdminUpdate) {
    return await this.unwrap(this.$http.put(this.getUrl(`/update/profile/${id}`), input), {
      transform: (d) => d.results
    })
  }
}
