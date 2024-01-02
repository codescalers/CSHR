import { ApiClientBase } from './base'

export class MyprofileApi extends ApiClientBase {
  protected readonly path = '/myprofile'

  async list() {}

  async update(id: number) {}
}
