import { ApiClientBase } from './base'
import type { Api } from '@/types'

export class EvaluationApi extends ApiClientBase {
  protected readonly path = '/evaluation'

  readonly users: EvaluationUsersApi

  constructor(options: Api.ClientOptions) {
    super(options)

    this.users = new EvaluationUsersApi(options, this.path)
  }

  async list() {}

  async create() {}
}

class EvaluationUsersApi extends ApiClientBase {
  protected readonly path = '/user'

  async list() {}

  async create() {}
}
