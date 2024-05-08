import { ApiClientBase } from './base'
import type { Api } from '@/types'

export class HrLettersApi extends ApiClientBase {
  protected readonly path = '/hr_letters'

  readonly approve: LettersApproveApi
  readonly reject: LettersRejectApi
  readonly user: LettersUserApi
  readonly docs: LettersDocsApi

  constructor(options: Api.ClientOptions) {
    super(options)

    this.approve = new LettersApproveApi(options, this.path)
    this.reject = new LettersRejectApi(options, this.path)
    this.user = new LettersUserApi(options, this.path)
    this.docs = new LettersDocsApi(options, this.path)
  }

  async list() {}

  async create() {}

  async read(id: number) {}

  async delete(id: number) {}
}

class LettersApproveApi extends ApiClientBase {
  protected readonly path = '/approve'

  async read(id: number) {}

  async update(id: number) {}
}

class LettersRejectApi extends ApiClientBase {
  protected readonly path = '/reject'

  async read(id: number) {}

  async update(id: number) {}
}

class LettersUserApi extends ApiClientBase {
  protected readonly path = '/user'

  async list() {}
}

class LettersDocsApi extends ApiClientBase {
  protected readonly path = '/docs'

  async list() {}

  async create() {}

  async read(id: number) {}
}
