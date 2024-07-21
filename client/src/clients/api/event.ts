import { ApiClientBase } from './base'
import type { Api } from '@/types'

export class EventApi extends ApiClientBase {
  protected readonly path = '/event'

  readonly exact: EventExactApi

  constructor(options: Api.ClientOptions) {
    super(options)

    this.exact = new EventExactApi(options, this.path)
  }

  async list(query?: any) {
    return this.unwrap(
      () => this.$http.get<Api.Returns.List<Api.Inputs.Event>>(this.getUrl('', query)),
      {
        transform: (d) => d.results
      }
    )
  }

  async create(input: Api.Inputs.Event) {
    ApiClientBase.assertUser()
    const event = await this.unwrap(
      () => this.$http.post<Api.Returns.Event>(this.getUrl(''), input),
      { transform: (d) => d.results }
    )

    return event
  }
}

class EventExactApi extends ApiClientBase {
  protected readonly path = '/exact'

  async list() {}
}
