import { ApiClientBase } from './base'

export class HomeApi extends ApiClientBase {
  protected readonly path = '/home'

  async list() {}
}
