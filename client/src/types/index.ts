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
  ME = 'me',
  ANOTHERUSER = 'anotheruser'
}

export enum CalendarEventSelection {
  PublicHoliday = 'Public Holiday',
  Birthday = 'Birthday',
  Vacation = 'Vacation',
  Event = 'Event',
  Meeting = 'Meeting',
  NewEvent = 'New Event'
}

export interface notificationType {
  id: number;
  body: string;
  receivers: number[];
  title: string;
  created_at: string;
  modified_at: string;
  is_read: boolean;
  link?: string;
  request: {
    id: number 
    reason: string
    status: string
    type: string
  }
}

export interface WSErrorType {
  code: number;
  message: string;
} 