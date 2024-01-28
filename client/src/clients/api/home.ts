import type { Api } from '@/types'
import { ApiClientBase } from './base'

export class HomeApi extends ApiClientBase {
  protected readonly path = '/home'

  async list(query?: any) {
    return this.unwrap(this.$http.get<Api.Returns.List<Api.Home>>(this.getUrl('', query)), {
      transform: (d) => d.results
    })
  }

 
}
