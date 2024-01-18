import type { Api } from '@/types'
import { ApiClientBase } from './base'

export class VacationsApi extends ApiClientBase {
  protected readonly path = '/vacations'

  readonly approve: VacationsApproveApi
  readonly reject: VacationsRejectApi
  readonly balance: VacationsBalanceApi
  readonly calculate: VacationsCalculateApi
  readonly comment: VacationsCommentApi
  readonly edit: VacationsEditApi
  readonly get_admin_balance: VacationsGetAdminBalanceApi
  readonly user: VacationsUserApi

  constructor(options: Api.ClientOptions) {
    super(options)

    this.approve = new VacationsApproveApi(options, this.path)
    this.reject = new VacationsRejectApi(options, this.path)
    this.balance = new VacationsBalanceApi(options, this.path)
    this.calculate = new VacationsCalculateApi(options, this.path)
    this.comment = new VacationsCommentApi(options, this.path)
    this.edit = new VacationsEditApi(options, this.path)
    this.get_admin_balance = new VacationsGetAdminBalanceApi(options, this.path)
    this.user = new VacationsUserApi(options, this.path)
  }

  async getVacationBalance(query?: any) {
    ApiClientBase.assertUser()
    const userBalance = await this.unwrap(
      this.$http.get<Api.Returns.Balance>(this.getUrl('/balance', query)),
      { transform: (d) => d.results }
    )
    return userBalance
  }
  async list() {}

  async create(input: Api.Inputs.Leave) {
    ApiClientBase.assertUser()
    const event = await this.unwrap(
      this.$http.post<Api.Returns.LeaveRequest>(this.getUrl(''), input),
      { transform: (d) => d.results }
    )

    return event
  }
  async read(id: number) {}

  async delete(id: number) {}
}

class VacationsApproveApi extends ApiClientBase {
  protected readonly path = '/approve'

  async update(id: number) {}
}

class VacationsRejectApi extends ApiClientBase {
  protected readonly path = '/reject'

  async read(id: number) {}

  async update(id: number) {}
}

class VacationsBalanceApi extends ApiClientBase {
  protected readonly path = '/balance'

  readonly adjustment: VacationsBalanceAdjustmentApi

  constructor(options: Api.ClientOptions, prePath: string) {
    super(options, prePath)

    this.adjustment = new VacationsBalanceAdjustmentApi(options, prePath + this.path)
  }

  async list() {}

  async update() {}
}

class VacationsBalanceAdjustmentApi extends ApiClientBase {
  protected readonly path = '/adjustment'

  async update() {}
}

class VacationsCalculateApi extends ApiClientBase {
  protected readonly path = '/calculate'

  async list() {}
}

class VacationsCommentApi extends ApiClientBase {
  protected readonly path = '/comment'

  async update(id: number) {}
}

class VacationsEditApi extends ApiClientBase {
  protected readonly path = '/edit'

  async read(id: number) {}

  async update(id: number) {}
}

class VacationsGetAdminBalanceApi extends ApiClientBase {
  protected readonly path = '/get-admin-balance'

  async list() {}

  async create(id: number) {}
}

class VacationsUserApi extends ApiClientBase {
  protected readonly path = '/user'

  async list(query?: any) {
    return this.unwrap(this.$http.get<Api.Returns.List<Api.Vacation>>(this.getUrl('', query)), {
      transform: (d) => d.results
    })
  }

}
