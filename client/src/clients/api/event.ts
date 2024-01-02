import { ApiClientBase, type ApiClientOptions } from './base'

export class EventApi extends ApiClientBase {
  protected readonly path = '/event'

  readonly exact: EventExactApi

  constructor(options: ApiClientOptions) {
    super(options)

    this.exact = new EventExactApi(options)
  }

  async list() {}

  async create() {}

  async read(id: number) {}

  async update(id: number) {}

  async delete(id: number) {}
}

class EventExactApi extends ApiClientBase {
  protected readonly path = '/event/exact'

  async list() {}
}
