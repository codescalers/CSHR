import { ApiClientBase } from './base'

export class TrainingCoursesApi extends ApiClientBase {
  protected readonly path = '/training_courses'

  async list() {}

  async create() {}

  async read(id: number) {}

  async update(id: number) {}

  async delete(id: number) {}
}