import { ApiClientBase } from './base'
import type { Api } from '@/types'

export class EventApi extends ApiClientBase {
  protected readonly path = '/event'

  readonly exact: EventExactApi

  constructor(options: Api.ClientOptions) {
    super(options)

    this.exact = new EventExactApi(options, this.path)
  }

  async list() {}

  async create() {}

  async read(id: number) {}

  async update(id: number) {}

  async delete(id: number) {}
}

class EventExactApi extends ApiClientBase {
  protected readonly path = '/exact'

  async list() {}
}
