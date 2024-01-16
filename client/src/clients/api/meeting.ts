import { ApiClientBase } from './base'
import type { Api } from '@/types'

export class MeetingApi extends ApiClientBase {
  protected readonly path = '/meeting'

  readonly exact: MeetingExactApi

  constructor(options: Api.ClientOptions) {
    super(options)

    this.exact = new MeetingExactApi(options)
  }

  async list() {}
  async create(input: Api.Inputs.Meeting) {
    ApiClientBase.assertUser()


    const event = await this.unwrap(
      this.$http.post<Api.Returns.Meeting>(this.getUrl('', input)),
      { transform: (d) => d.results }
    )

    return event
  }

  async read(id: number) {}

  async update(id: number) {}

  async delete(id: number) {}
}

class MeetingExactApi extends ApiClientBase {
  protected readonly path = '/exact'

  async list() {}
}
