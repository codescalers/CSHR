import { ApiClientBase } from './base'

export class ProfileApi extends ApiClientBase {
  protected readonly path = '/myprofile'

  async list() {}

  async update(id: number) {}
}
