import { ApiClientBase } from './base'

export class CompanyPropertiesApi extends ApiClientBase {
  protected readonly path = `/company_properties`

  async list() {}

  async create() {}

  async read(id: number) {}

  async update(id: number) {}

  async delete(id: number) {}
}