export * from './api'


export interface Country {
    id: number
    country: string
}

export interface JWTokenObject {
    token_type: string
    exp: number
    iat: number
    jti: string
    user_id: number
}

export enum Selection {
    ME = "me",
    ANOTHERUSER = "anotheruser",
  }