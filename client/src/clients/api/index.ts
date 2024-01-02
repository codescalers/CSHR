import type { NotifierService } from 'vue3-notifier'

import { ApiClientBase } from './base'
import type { Api } from '@/types'

import { AuthApi } from './auth'
import { CompanyPropertiesApi } from './company_properties'
import { CompensationsApi } from './compensations'
import { EvaluationApi } from './evaluation'
import { EventApi } from './event'
import { HomeApi } from './home'
import { HrLettersApi } from './hr_letters'
import { MeetingApi } from './meeting'
import { MyprofileApi } from './myprofile'
import { NotificationsApi } from './notifications'
import { RequestsApi } from './requests'
import { OfficeApi } from './office'
import { TrainingCoursesApi } from './training_courses'
import { OfficialDocumentsApi } from './official_documents'
import { UsersApi } from './users'
import { VacationsApi } from './vacations'

export class ApiClient extends ApiClientBase {
  protected readonly path = '/'

  private readonly requestInterceptorId: number
  private readonly responseInterceptorId: number

  readonly auth: AuthApi
  readonly company_properties: CompanyPropertiesApi
  readonly compensations: CompensationsApi
  readonly evaluation: EvaluationApi
  readonly event: EventApi
  readonly home: HomeApi
  readonly hr_letters: HrLettersApi
  readonly meeting: MeetingApi
  readonly myprofile: MyprofileApi
  readonly notifications: NotificationsApi
  readonly requests: RequestsApi
  readonly office: OfficeApi
  readonly training_courses: TrainingCoursesApi
  readonly official_documents: OfficialDocumentsApi
  readonly users: UsersApi
  readonly vacations: VacationsApi

  constructor(options: Api.ClientOptions) {
    super(options)
    this.requestInterceptorId = this.setAxiosRequestInterceptor()
    this.responseInterceptorId = this.setAxiosResponseInterceptor()

    this.auth = new AuthApi(options)
    this.company_properties = new CompanyPropertiesApi(options)
    this.compensations = new CompensationsApi(options)
    this.evaluation = new EvaluationApi(options)
    this.event = new EventApi(options)
    this.home = new HomeApi(options)
    this.hr_letters = new HrLettersApi(options)
    this.meeting = new MeetingApi(options)
    this.myprofile = new MyprofileApi(options)
    this.notifications = new NotificationsApi(options)
    this.requests = new RequestsApi(options)
    this.office = new OfficeApi(options)
    this.training_courses = new TrainingCoursesApi(options)
    this.official_documents = new OfficialDocumentsApi(options)
    this.users = new UsersApi(options)
    this.vacations = new VacationsApi(options)
  }

  setNotifier(service: NotifierService) {
    if (!ApiClientBase.$notifier) {
      ApiClientBase.$notifier = service
    }
  }

  private setAxiosRequestInterceptor() {
    return this.$http.interceptors.request.use((req) => {
      if (ApiClientBase.user) {
        req.headers.set('Authorization', 'Bearer ' + ApiClientBase.user.access_token)
      }
      return req
    })
  }

  private setAxiosResponseInterceptor() {
    return this.$http.interceptors.response.use((res) => {
      console.log('[TODO] response intercetpor', res)
      return res
    })
  }

  disconnect() {
    this.$http.interceptors.request.eject(this.requestInterceptorId)
    this.$http.interceptors.response.eject(this.responseInterceptorId)
  }
}
