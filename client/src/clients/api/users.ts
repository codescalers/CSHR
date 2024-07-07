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
  readonly supervisors: UsersSupervisorsApi

  constructor(options: Api.ClientOptions) {
    super(options)

    this.admin = new UsersAdminApi(options, this.path)
    this.birthdates = new UsersBirthdatesApi(options, this.path)
    this.set_active = new UsersSetActiveApi(options, this.path)
    this.set_inactive = new UsersSetInActiveApi(options, this.path)
    this.skills = new UsersSkillsApi(options, this.path)
    this.team = new UsersTeamApi(options, this.path)
    this.supervisors = new UsersSupervisorsApi(options, this.path)
  }

  list(query?: any) {
    return this.unwrap(() => this.$http.get<Api.Returns.List<Api.User>>(this.getUrl('', query)))
  }
  getuser(id: number, options: Api.UnwrapOptions<any, any> = {}): Promise<Api.User> {
    return this.unwrap(() => this.$http.get<Api.Returns.Profile>(this.getUrl(`/${id}`)), {
      transform: (d) => d.results,
      ...options
    })
  }
  read(id: number) {
    return this.unwrap(() => this.$http.get<Api.Returns.MsgRes<Api.User>>(this.getUrl(`/${id}`)), {
      transform: (d) => d.results
    })
  }
}

class UsersAdminApi extends ApiClientBase {
  protected readonly path = '/admin'

  readonly office_users: UsersAdminofficeUsersApi

  constructor(options: Api.ClientOptions, prePath: string) {
    super(options, prePath)

    this.office_users = new UsersAdminofficeUsersApi(options, prePath + this.path)
  }

  list(query?: Api.Inputs.List) {
    return this.unwrap(() => this.$http.get<Api.Returns.List<Api.User>>(this.getUrl('', query)))
  }

  read(id: number) {
    return this.unwrap(() => this.$http.get<Api.Returns.MsgRes<Api.User>>(this.getUrl(`/${id}`)), {
      transform: (d) => d.results
    })
  }

  update(id: number, input: Api.Inputs.UsersAdminUpdate) {
    return this.unwrap(
      () => this.$http.put<Api.Returns.MsgRes<Api.AdminUser>>(this.getUrl(`/${id}`), input),
      { transform: (d) => d.results }
    )
  }

  delete(id: number) {
    return this.unwrap(() => this.$http.delete<void>(this.getUrl(`/${id}`)))
  }
}

class UsersAdminofficeUsersApi extends ApiClientBase {
  protected readonly path = '/office_users'

  list(query?: Api.Inputs.List) {
    return this.unwrap(() => this.$http.get(this.getUrl('', query)))
  }
}

class UsersBirthdatesApi extends ApiClientBase {
  protected readonly path = '/birthdates'

  list() {}
}

class UsersSetActiveApi extends ApiClientBase {
  protected readonly path = '/set_active'

  update(input: Api.Inputs.UsersActive) {
    return this.unwrap(() => this.$http.put<any>(this.getUrl(), input))
  }
}

class UsersSetInActiveApi extends ApiClientBase {
  protected readonly path = '/set_inactive'

  update(input: Api.Inputs.UsersActive) {
    return this.unwrap(() => this.$http.put<any>(this.getUrl(), input))
  }
}

class UsersSkillsApi extends ApiClientBase {
  protected readonly path = '/skills'

  list(query?: Api.Inputs.List) {
    return this.unwrap(() => this.$http.get<Api.Returns.List<Api.Skill>>(this.getUrl('', query)))
  }

  create(input: Api.Inputs.UserSkills) {
    return this.unwrap(() =>
      this.$http.post<Api.Inputs.UserSkills>(this.getUrl('/add_skill'), input)
    )
  }
}

class UsersSupervisorsApi extends ApiClientBase {
  protected readonly path = '/supervisors'

  async list( query?: Api.Inputs.List) {
    ApiClientBase.assertUser()
    return this.unwrap(() => this.$http.get<Api.Returns.List<Api.User>>(this.getUrl("", query)))
  }
}

class UsersTeamApi extends ApiClientBase {
  protected readonly path = '/team'

  readonly supervisors: UsersTeamSupervisorsApi

  constructor(options: Api.ClientOptions, prePath: string) {
    super(options, prePath)

    this.supervisors = new UsersTeamSupervisorsApi(options, prePath + this.path)
  }

  list(query?: any) {
      return this.unwrap(() => this.$http.get<Api.Returns.List<Api.User>>(this.getUrl('', query)))
  }
}

class UsersTeamSupervisorsApi extends ApiClientBase {
  protected readonly path = '/supervisors'

  async list(query?: Api.Inputs.List) {
    return await this.unwrap(
      () => this.$http.get<Api.Returns.List<Api.User>>(this.getUrl('', query)),
      {
        transform: (d) => d.results
      }
    )
  }
}
