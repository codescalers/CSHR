import type { Api } from '@/types'
import { ApiClientBase } from './base'

export class NotificationsApi extends ApiClientBase {
  protected readonly path = '/notifications'

  list() {
    ApiClientBase.assertUser()
    return this.unwrap(this.$http.get<{ results: Api.Returns.Notification[] }>(this.path), {
      transform: (d) => d.results
    })
  }

  async read(type: string, id: number) {
    ApiClientBase.assertUser()
    const notification = await this.unwrap(this.$http.get(`${type}/${id}`), {
      transform: (d) => d.results
    })

    return notification
  }
}
