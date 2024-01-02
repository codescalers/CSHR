import type { AxiosError, AxiosInstance, AxiosResponse } from 'axios'

export module Api {
  export interface ClientOptions {
    $http: AxiosInstance
  }

  export type Path = `/${string}`
  export type LoginUser = Api.Returns.Login['results']

  export interface UnwrapOptions<T, R> {
    transform?: (data: T, res: AxiosResponse<T, any>) => R
    normalizeError?: (error: AxiosError<any>, res: AxiosResponse<T>) => string
  }

  export interface User {
    /* Code */
  }

  export module Returns {
    export interface Login {
      message: string
      results: {
        id: number
        email: string
        refresh_token: string
        access_token: string
        full_name: string
        first_name: string
        last_name: string
      }
    }

    export interface Register {
      message: string
      results: Api.Inputs.Register
    }

    export interface Refresh {
      access: string
      refresh: string
    }
  }

  export module Inputs {
    /**
     * @description
     * `YYYY-MM-DD`
     */
    export type DashedDate = `${number}-${number}-${number}`
    export type Teams = "Business Development" | "Development" | "HR & Finance" | "QA" | "Marketing" | "Operations" | "Support" // prettier-ignore
    export type Users = 'Admin' | 'User' | 'Supervisor'
    export type Gender = 'Male' | 'Female'

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
      salary?: {}
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
  }
}
