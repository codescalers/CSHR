import { ApiClientBase, type ApiClientOptions } from './base'

import { AuthApi } from './auth'
import { CompaniesApi } from './companies'
import { CompensationsApi } from './compensations'
import { EventApi } from './event'
import { HomeApi } from './home'
import { LettersApi } from './letters'
import { MeetingApi } from './meeting'
import { ProfileApi } from './profile'
import { NotificationsApi } from './notifications'
import { RequestsApi } from './requests'
import { OfficeApi } from './office'
import { CoursesApi } from './courses'

export class ApiClient extends ApiClientBase {
  protected readonly path = '/'
  private readonly interceptorId: number

  readonly auth: AuthApi
  readonly companies: CompaniesApi
  readonly compensations: CompensationsApi
  readonly event: EventApi
  readonly home: HomeApi
  readonly letters: LettersApi
  readonly meeting: MeetingApi
  readonly profile: ProfileApi
  readonly notifications: NotificationsApi
  readonly requests: RequestsApi
  readonly office: OfficeApi
  readonly courses: CoursesApi

  constructor(options: ApiClientOptions) {
    super(options)
    this.interceptorId = this.setAxiosInterceptor()

    this.auth = new AuthApi(options)
    this.companies = new CompaniesApi(options)
    this.compensations = new CompensationsApi(options)
    this.event = new EventApi(options)
    this.home = new HomeApi(options)
    this.letters = new LettersApi(options)
    this.meeting = new MeetingApi(options)
    this.profile = new ProfileApi(options)
    this.notifications = new NotificationsApi(options)
    this.requests = new RequestsApi(options)
    this.office = new OfficeApi(options)
    this.courses = new CoursesApi(options)
  }

  private setAxiosInterceptor() {
    return this.$http.interceptors.request.use((req) => {
      if (ApiClientBase.ACCESS_TOKEN) {
        req.headers.set('Authorization', 'Bearer ' + ApiClientBase.ACCESS_TOKEN)
      }
      return req
    })
  }

  disconnect() {
    this.$http.interceptors.request.eject(this.interceptorId)
  }
}
