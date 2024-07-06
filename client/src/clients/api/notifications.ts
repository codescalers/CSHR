import type { Api, notificationType } from '@/types'
import { ApiClientBase } from './base'

export class NotificationsApi extends ApiClientBase {
  protected readonly path = '/notifications'

  list() {
    ApiClientBase.assertUser()
    return this.unwrap(() => this.$http.get<{ results: notificationType[] }>(this.path), {
      transform: (d) => d.results
    })
  }

  readAllNotifications(userID: number) {
    ApiClientBase.assertUser()
    return this.unwrap(() => this.$http.put<{ results: notificationType[] }>(`${this.path}/read-all/${userID}/`), {
      transform: (d) => d.results
    })
  }

  deleteAllNotifications(userID: number) {
    ApiClientBase.assertUser()
    return this.unwrap(() => this.$http.delete<{ results: notificationType[] }>(`${this.path}/delete-all/${userID}/`), {
      transform: (d) => d.results
    })
  }

  async getNotification(id: number) {
    ApiClientBase.assertUser()
    const notification = await this.unwrap(() => this.$http.get(`${this.path}/${id}/`), {
      transform: (d) => d.results
    })

    return notification
  }

  async readNotification(id: number, isRead: boolean) {
    ApiClientBase.assertUser()
    const notification = await this.unwrap(
      () => this.$http.put(`${this.path}/${id}/`, { is_read: isRead }),
      {
        transform: (d) => d.results
      }
    )

    return notification
  }
}
