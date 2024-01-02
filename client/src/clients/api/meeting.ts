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

  async create() {}

  async read(id: number) {}

  async update(id: number) {}

  async delete(id: number) {}
}

class MeetingExactApi extends ApiClientBase {
  protected readonly path = '/exact'

  async list() {}
}
