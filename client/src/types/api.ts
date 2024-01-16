import type { AxiosError, AxiosInstance, AxiosResponse } from 'axios'

export module Api {
  /**
   * @description
   * `YYYY-MM-DD`
   */
  export type DashedDate = `${number}-${number}-${number}`
  export type Teams = "Business Development" | "Development" | "HR & Finance" | "QA" | "Marketing" | "Operations" | "Support" // prettier-ignore
  export type Users = 'Admin' | 'User' | 'Supervisor'
  export type Gender = 'Male' | 'Female'

  export interface ClientOptions {
    $http: AxiosInstance
  }

  export type Path = `/${string}`
  export type LoginUser = Api.Returns.Login['results']

  export interface UnwrapOptions<T, R> {
    transform?: (data: T, res: AxiosResponse<T, any>) => R
    normalizeError?: (error: AxiosError<any>, res: AxiosResponse<T>) => string
  }

  export interface Skill {
    name: string
  }

  export interface Certificate {}

  export interface Salary {}

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
    export type Login = MsgRes<{
      id: number
      email: string
      refresh_token: string
      access_token: string
      full_name: string
      first_name: string
      last_name: string
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
      event_id: number
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
  }
  export module Inputs {
    export interface Event {
      name: string
      description: string
      from_date: string
      end_date: string
    }

    export interface Meeting {
      date: string
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

    export type UserSkills = { skills: string[] }
  }
}
