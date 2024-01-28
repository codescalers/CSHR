import moment from 'moment'

import type { JWTokenObject } from "@/types"

export async function resolve<T>(promise: Promise<T>): Promise<[T, any]> {
  try {
    return [await promise, null]
  } catch (error) {
    return [null as T, error]
  }
}

export function panic(msg: string, devLogs?: any[]): never {
  devLogs && devLog(...devLogs)
  throw new Error(msg)
}

export function devLog(...args: any[]): void {
  import.meta.env.DEV && args.length > 0 && console.log(...args)
}

export const DASHBOARD_ITEMS = [
  { id: 1, name: 'Set Vacations' },
  { id: 2, name: 'Set User Vacations' },
  // { id: 3, name: 'Update Office Vacations' },
  { id: 4, name: 'Add Office' },
  { id: 5, name: 'Add User' },
  { id: 6, name: 'Update User Profile' }
]

export const formatDate = (date: any) => moment(date).format('YYYY-MM-DD')

export function getStatusColor(status: string) {
  switch (status) {
    case 'vacations':
    case 'approved':
      return 'green'

    case 'hr_letters':
    case 'pending':
      return 'orange'

    case 'rejected':
      return 'red'

    default:
      return 'grey'
  }
}
export function decodeAccessToken(token: string): JWTokenObject {
  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
  return JSON.parse(jsonPayload);
}

export function isValidToken(token: string): boolean{
  return Date.now() >= decodeAccessToken(token).exp * 1000
}