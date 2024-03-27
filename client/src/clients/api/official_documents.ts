import { ApiClientBase } from './base'

import type { Api } from '@/types'

export class OfficialDocumentsApi extends ApiClientBase {
  protected readonly path = '/official_documents'

  readonly approve: OfficialDocumentsApproveApi
  readonly reject: OfficialDocumentsRejectApi

  constructor(options: Api.ClientOptions) {
    super(options)

    this.approve = new OfficialDocumentsApproveApi(options)
    this.reject = new OfficialDocumentsRejectApi(options)
  }

  async create() {}
}

class OfficialDocumentsApproveApi extends ApiClientBase {
  protected readonly path = '/official_documents/approve'

  async update(id: number) {}
}

class OfficialDocumentsRejectApi extends ApiClientBase {
  protected readonly path = '/official_documents/reject'

  async update(id: number) {}
}
