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
  readonly post_admin_balance: VacationsPostAdminBalanceApi
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
    this.post_admin_balance = new VacationsPostAdminBalanceApi(options, this.path)
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

  async create() {}

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

  async list(query: Api.Inputs.UserId) {
    return this.unwrap(this.$http.get(this.getUrl('', query)), { transform: (d) => d.results })
  }

  async update(query: Api.Inputs.UserId, input: Api.Inputs.Vacation) {
    return this.unwrap(this.$http.put(this.getUrl('', query), input), {
      transform: (d) => d.results
    })
  }
}

class VacationsBalanceAdjustmentApi extends ApiClientBase {
  protected readonly path = '/adjustment'

  async update(input: Api.Inputs.BalanceAdjustment) {
    ApiClientBase.assertUser()
    return await this.unwrap(this.$http.put(this.getUrl(), input), {
      transform: (d) => d.results
    })
  }
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

  constructor(options: Api.ClientOptions, prePath: string) {
    super(options, prePath)
  }
  async list() {
    ApiClientBase.assertUser()
    return await this.unwrap(this.$http.get(this.getUrl()), {
      transform: (d) => d.results
    })
  }
}

class VacationsPostAdminBalanceApi extends ApiClientBase {
  protected readonly path = '/post-admin-balance'

  async create(input: Api.Inputs.Vacations) {
    ApiClientBase.assertUser()
    return await this.unwrap(this.$http.post(this.getUrl(), input), {
      transform: (d) => d.results
    })
  }
}

class VacationsUserApi extends ApiClientBase {
  protected readonly path = '/user'

  async list() {}
}
