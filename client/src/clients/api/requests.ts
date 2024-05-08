import { ApiClientBase } from './base'

export class RequestsApi extends ApiClientBase {
  protected readonly path = '/requests'

  async list() {}
}
