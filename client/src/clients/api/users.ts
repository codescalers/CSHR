import type { Api } from '@/types'
import { ApiClientBase } from './base'

export class UsersApi extends ApiClientBase {
  protected readonly path = '/users'

  readonly admin: UsersAdminApi
  readonly birthdates: UsersBirthdatesApi
  readonly set_active: UsersSetActiveApi
  readonly set_inactive: UsersSetInActiveApi
  readonly skills: UsersSkillsApi
  readonly team: UsersTeamApi

  constructor(options: Api.ClientOptions) {
    super(options)

    this.admin = new UsersAdminApi(options, this.path)
    this.birthdates = new UsersBirthdatesApi(options, this.path)
    this.set_active = new UsersSetActiveApi(options, this.path)
    this.set_inactive = new UsersSetInActiveApi(options, this.path)
    this.skills = new UsersSkillsApi(options, this.path)
    this.team = new UsersTeamApi(options, this.path)
  }

  async list() {}

  async read(id: number) {}
}

class UsersAdminApi extends ApiClientBase {
  protected readonly path = '/admin'

  readonly office_users: UsersAdminofficeUsersApi

  constructor(options: Api.ClientOptions, prePath: string) {
    super(options, prePath)

    this.office_users = new UsersAdminofficeUsersApi(options, prePath + this.path)
  }

  async list() {}

  async read(id: number) {}

  async update(id: number) {}

  async delete(id: number) {}
}

class UsersAdminofficeUsersApi extends ApiClientBase {
  protected readonly path = '/office_users'

  async list() {}
}

class UsersBirthdatesApi extends ApiClientBase {
  protected readonly path = '/birthdates'

  async list() {}
}

class UsersSetActiveApi extends ApiClientBase {
  protected readonly path = '/set_active'

  async update() {}
}

class UsersSetInActiveApi extends ApiClientBase {
  protected readonly path = '/set_inactive'

  async update() {}
}

class UsersSkillsApi extends ApiClientBase {
  protected readonly path = '/skills'

  async list() {}

  async create() {}
}

class UsersTeamApi extends ApiClientBase {
  protected readonly path = '/team'

  readonly supervisors: UsersTeamSupervisorsApi

  constructor(options: Api.ClientOptions, prePath: string) {
    super(options, prePath)

    this.supervisors = new UsersTeamSupervisorsApi(options, prePath + this.path)
  }

  async list() {}
}

class UsersTeamSupervisorsApi extends ApiClientBase {
  protected readonly path = '/supervisors'

  async list() {}
}
