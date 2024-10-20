import type { Api } from '@/types'
import { ApiClientBase } from './base'

export class OfficeApi extends ApiClientBase {
  protected readonly path = '/office'

  async list(query?: any) {
    ApiClientBase.assertUser()
    return this.unwrap(() => this.$http.get<Api.Returns.List<Api.LocationType>>(this.getUrl('', query)), {
      transform: (d) => d
    })
  }

  async officeHolidays(query: {year: number, office_id: number} ) {
    ApiClientBase.assertUser()
    return this.unwrap(() => this.$http.get<Api.Returns.List<Api.OfficeHolidayDates>>(
      this.getUrl(`/holidays`, query)
    ), {
      transform: (d) => d.results
    })
  }

  async create(input: Api.Inputs.Office) {
    ApiClientBase.assertUser()
    return this.unwrap(() => this.$http.post(this.getUrl(), input), {
      transform: (d) => d.results
    })
  }

  async read(id: number) {
    ApiClientBase.assertUser()
    return this.unwrap(() => this.$http.get(this.getUrl(`/${id}`)), {
      transform: (d) => d.results
    })
  }
}
