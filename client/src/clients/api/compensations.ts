import { ApiClientBase, type ApiClientOptions } from './base'

export class CompensationsApi extends ApiClientBase {
  protected readonly path = '/compensations'

  readonly approve: CompensationsApproveApi
  readonly reject: CompensationsRejectApi
  readonly user: CompensationsUserApi

  constructor(options: ApiClientOptions) {
    super(options)

    this.approve = new CompensationsApproveApi(options)
    this.reject = new CompensationsRejectApi(options)
    this.user = new CompensationsUserApi(options)
  }

  async list() {}

  async create() {}

  async read(id: number) {}

  async delete(id: number) {}
}

class CompensationsApproveApi extends ApiClientBase {
  protected readonly path = '/compensations/approve'

  async read(id: number) {}

  async update(id: number) {}
}

class CompensationsRejectApi extends ApiClientBase {
  protected readonly path = '/compensations/reject'

  async read(id: number) {}

  async update(id: number) {}
}

class CompensationsUserApi extends ApiClientBase {
  protected readonly path = '/user'

  async list() {}
}
