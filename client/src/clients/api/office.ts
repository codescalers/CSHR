import { ApiClientBase } from './base'

export class OfficeApi extends ApiClientBase {
  protected readonly path = '/office'

  async list() {}

  async create() {}

  async read(id: number) {}

  async update(id: number) {}

  async delete(id: number) {}
}
