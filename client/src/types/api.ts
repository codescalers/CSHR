import type { AxiosError, AxiosInstance, AxiosResponse } from 'axios'

export module Api {
  /**
   * @description
   * `YYYY-MM-DD`
   */
  export type DashedDate = `${number}-${number}-${number}`
  export type Teams = "Business Development" | "Development" | "HR & Finance" | "QA" | "Marketing" | "Operations" | "Support" // prettier-ignore
  export type Users = 'Admin' | 'User' | 'Team Lead'
  export type Gender = 'Male' | 'Female'

  export interface ClientOptions {
    $http: AxiosInstance
  }

  export type Path = `/${string}`
  export type LoginUser = Api.Returns.Login['results'] & { fullUser: Api.User }

  export interface UnwrapOptions<T, R> {
    transform?: (data: T, res: AxiosResponse<T, any>) => R
    normalizeError?: (error: AxiosError<any>, res: AxiosResponse<T>) => string
    disableNotify?: boolean
  }

  export interface Skill {
    name: string
  }

  export interface Vacation {
    id: number
    created_at: any
    modified_at: any
    type: string
    status: string
    reason: string
    from_date: any
    end_date: any
    change_log: any[]
    actual_days: number
    applying_user: number | any
    approval_user: number
    user?: Api.User
    isUpdated?: boolean
  }

  export interface LeaveReason {
    name: string
    reason: string
  }

  export interface Certificate {}

  export interface Salary {}
  export interface Meetings {
    id: number
    invited_users: any[]
    date: any
    meeting_link: string
    host_user: {
      id: number
      full_name: string
      email: string
      image: string
      team: string
      gender: string
      skills: []
      job_title: string
      user_certificates: any[]
    }
    location: string
  }
  export interface User {
    id: number
    first_name: string
    last_name: string
    full_name: string
    email: string
    gender: Gender
    team: string
    image: string
    telegram_link: string
    social_insurance_number: string
    mobile_number: string
    reporting_to: number[]
    birthday: string
    location: {
      id: number
      name: string
      country: string
      weekend: string
    }
    skills: Skill[]
    user_certificates: Certificate[]
    joining_at: string
    job_title: string
    address: string
    user_type: string
    background_color: string
    is_active: boolean
  }

  export interface BalanceVacation {
    sick_leaves: {
      reserved: number
      all: string
    }
    compensation: {
      reserved: number
      all: string
    }
    unpaid: {
      reserved: number
      all: string
    }
    annual_leaves: {
      reserved: number
      all: string
    }
    emergency_leaves: {
      reserved: number
      all: string
    }
    leave_excuses: {
      reserved: number
      all: string
    }
  }
  export interface AdminUser extends Omit<'User', 'is_active'> {
    user_company_properties: 'string'
    salary: Salary
    user_evaluation: string
    user_type: 'Admin'
  }

  export module Returns {
    export interface MsgRes<T> {
      message: string
      results: T
    }
    export type Event = MsgRes<Event>
    export type Meeting = MsgRes<Meeting>

    export type Profile = MsgRes<User>
    export type AllMeetings = MsgRes<Meetings>

    export type Login = MsgRes<{
      id: number
      email: string
      refresh_token: string
      access_token: string
      full_name: string
      first_name: string
      last_name: string
    }>

    export type LeaveRequest = MsgRes<{
      title: string
      className: string
      eventName: string
      vacation: {
        id: number
        reason: string
        from_date: any
        end_date: any
        status: string
        applying_user: {
          id: number
          full_name: string
          email: string
          image: string
          team: string
          gender: string
          skills: []
          job_title: string
          user_certificates: []
        }
        approval_user: {
          email: string
          team: string
          gender: string
          job_title: string
        }
        change_log: {}
        type: string
      }

      len: number
      date: any
    }>

    export type Balance = MsgRes<BalanceVacation>

    export interface Register {
      message: string
      results: Api.Inputs.Register
    }

    export interface Refresh {
      access: string
      refresh: string
    }

    export interface List<T> {
      count: number
      previous: string | null
      next: string | null
      results: T[]
    }

    export interface Notification {
      type: string
      title: string
      created_at: string
      event_id: string
      user: {
        id: number
        full_name: string
        email: string
        image: string
        team: string
        gender: Gender
        skills: Skill[]
        job_title: string
        user_certificates: Certificate[]
      }
    }

    export interface GetAdminBalance {
      annual_leaves: number
      compensation: number
      emergency_leaves: number
      leave_excuses: number
      year: number
      public_holidays: Date[]
      location: {
        id: number
        name: string
        country: string
        weekend: string
      }
    }
  }
  export interface Holiday {
    id: number
    location: {
      id: number
      name: string
      country: string
      weekend: string
    }
    holiday_date: any
    expired: boolean
  }

  export interface Home {
    id: number
    title: string
    className: string
    eventName: string
    vacation?: any
    meeting?: any
    event?: any
    holidays?: any
    users?: any
    date: any
    len?: number
  }

  export module Inputs {
    export interface Event {
      name: string
      description: string
      from_date: any
      end_date: any
    }

    export interface Leave {
      reason: string | undefined
      from_date: any
      end_date: any
      actual_days?: number
    }

    export interface ActualDays {
      start_date: any
      end_date: any
    }
    export interface Meeting {
      date: any
      meeting_link: string
      location: string
    }

    export interface Login {
      email: string
      password: string
    }

    export interface Register {
      first_name: string
      last_name: string
      telegram_link: string
      email: string
      birthday: DashedDate
      joining_at: DashedDate
      mobile_number: string
      password: string
      location: number
      team: Teams
      salary?: Salary
      user_type: Users
      reporting_to?: number[]
      gender: Gender
      job_title: string
      address: string
      social_insurance_number: string
      image?: string
    }

    export interface Refresh {
      refresh: string
    }

    export interface ChangePassword {
      old_password: string
      new_password: string
    }

    export type List = { page?: number }

    export interface UsersAdminUpdate {
      gender: string
      email: string
      telegram_link: string
      birthday: string
      joining_at: string
      social_insurance_number: string
      team: string
      salary?: Salary
      mobile_number: string
      job_title: string
      address: string
      user_type: Users
    }

    export type UsersActive = { user_id: number }

    export type UserId = { user_ids: number }

    export type UserSkills = { skills: string[] }

    export type Vacations = {
      annual_leaves: number
      compensation: number
      emergency_leaves: number
      leave_excuses: number
      year: number
      public_holidays: string[]
    }

    export type BalanceAdjustment = {
      officeId: number
      value: number
      reason: string
    }

    export type Office = {
      name: string
      country: string
      weekend: string
    }

    export type Vacation = {
      annual_leaves: number
      emergency_leaves: number
      leave_excuses: number
    }
  }
}
