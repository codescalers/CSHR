import type { Api } from '@/types'
import { ApiClientBase } from './base'

export class OfficeApi extends ApiClientBase {
  protected readonly path = '/office'

  async list() {
    ApiClientBase.assertUser()
    return this.unwrap(() => this.$http.get(this.getUrl()), {
      transform: (d) => d.results
    })
  }

  async create(input: Api.Inputs.Office) {
    ApiClientBase.assertUser()
    return this.unwrap(() => this.$http.post(this.getUrl(), input), {
      transform: (d) => d.results
    })
  }

  async read(id: number) {
    ApiClientBase.assertUser()
    return this.unwrap(() => this.$http.get(this.getUrl(`/${id}`)), {
      transform: (d) => d.results
    })
  }

  async update(id: number) {}

  async delete(id: number) {}
}
