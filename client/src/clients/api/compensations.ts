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
}

class CompensationsApproveApi extends ApiClientBase {
  protected readonly path = '/approve'
}

class CompensationsRejectApi extends ApiClientBase {
  protected readonly path = '/reject'
}

class CompensationsUserApi extends ApiClientBase {
  protected readonly path = '/user'

  async list() {}
}
