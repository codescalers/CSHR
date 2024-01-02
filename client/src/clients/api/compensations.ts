import { ApiClientBase } from './base'
import type { Api } from '@/types'

export class CompensationsApi extends ApiClientBase {
  protected readonly path = '/compensations'

  readonly approve: CompensationsApproveApi
  readonly reject: CompensationsRejectApi
  readonly user: CompensationsUserApi

  constructor(options: Api.ClientOptions) {
    super(options)

    this.approve = new CompensationsApproveApi(options, this.path)
    this.reject = new CompensationsRejectApi(options, this.path)
    this.user = new CompensationsUserApi(options, this.path)
  }

  async list() {}

  async create() {}

  async read(id: number) {}

  async delete(id: number) {}
}

class CompensationsApproveApi extends ApiClientBase {
  protected readonly path = '/approve'

  async read(id: number) {}

  async update(id: number) {}
}

class CompensationsRejectApi extends ApiClientBase {
  protected readonly path = '/reject'

  async read(id: number) {}

  async update(id: number) {}
}

class CompensationsUserApi extends ApiClientBase {
  protected readonly path = '/user'

  async list() {}
}
