import { ApiClientBase, type ApiClientOptions } from './base'

export class MeetingApi extends ApiClientBase {
  protected readonly path = '/meeting'

  readonly exact: MeetingExactApi

  constructor(options: ApiClientOptions) {
    super(options)

    this.exact = new MeetingExactApi(options)
  }

  async list() {}

  async create() {}

  async read(id: number) {}

  async update(id: number) {}

  async delete(id: number) {}
}

class MeetingExactApi extends ApiClientBase {
  protected readonly path = '/meeting/exact'

  async list() {}
}
