import { ApiClientBase, type ApiClientOptions } from './base'

export class LettersApi extends ApiClientBase {
  protected readonly path = '/hr_letters'

  readonly approve: LettersApproveApi
  readonly reject: LettersRejectApi
  readonly user: LettersUserApi
  readonly docs: LettersDocsApi

  constructor(options: ApiClientOptions) {
    super(options)

    this.approve = new LettersApproveApi(options)
    this.reject = new LettersRejectApi(options)
    this.user = new LettersUserApi(options)
    this.docs = new LettersDocsApi(options)
  }

  async list() {}

  async create() {}

  async read(id: number) {}

  async delete(id: number) {}
}

class LettersApproveApi extends ApiClientBase {
  protected readonly path = '/hr_letters/approve'

  async read(id: number) {}

  async update(id: number) {}
}

class LettersRejectApi extends ApiClientBase {
  protected readonly path = '/hr_letters/reject'

  async read(id: number) {}

  async update(id: number) {}
}

class LettersUserApi extends ApiClientBase {
  protected readonly path = '/hr_letters/user'

  async list() {}
}

class LettersDocsApi extends ApiClientBase {
  protected readonly path = '/hr_letters/docs'

  async list() {}

  async create() {}

  async read(id: number) {}
}
