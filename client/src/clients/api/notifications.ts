import { ApiClientBase } from './base'

export class NotificationsApi extends ApiClientBase {
  protected readonly path = '/notifications'

  async list() {
    ApiClientBase.assertUser()
    const notifications = await this.unwrap(this.$http.get(this.path), {
      transform: (d) => d.results
    })

    return notifications
  }

  async read(type: string, id: number) {
    ApiClientBase.assertUser()
    const notification = await this.unwrap(this.$http.get(`${type}/${id}`), {
      transform: (d) => d.results
    })

    return notification
  }
}
