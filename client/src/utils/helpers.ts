import moment from 'moment'

import type { Api } from "@/types"
import type { JWTokenObject } from "@/types"
import type { ApiClient } from '@/clients/api'
import { capitalize, ref } from 'vue'

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

export const DASHBOARD_ITEMS = ref([
  { id: 1, name: 'Set Vacations', active: true, },
  { id: 2, name: 'Set User Vacations', active: false, },
  // { id: 3, name: 'Update Office Vacations' },
  { id: 4, name: 'Add Office', active: false, },
  { id: 5, name: 'Add User', active: false, },
  { id: 6, name: 'Update User Profile', active: false, }
])

export const formatDate = (date: any) => moment(date).format('YYYY-MM-DD')

export function formatDateTime(dateString: string) {
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    year: 'numeric', month: 'long', day: 'numeric',
    hour: 'numeric', minute: 'numeric', second: 'numeric',
    hour12: true
  }).replace(' at', '');
}

export const fieldRequired = [(v: string) => !!v || 'Field is required.']

export function validURL(value: string) {
  const pattern = new RegExp('^(https?:\\/\\/)?'+
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+
    '((\\d{1,3}\\.){3}\\d{1,3}))'+
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+
    '(\\?[;&a-z\\d%_.~+=-]*)?'+
    '(\\#[-a-z\\d_]*)?$','i');
  return !!pattern.test(value) || 'Please enter a vlaid URL.';
}

export function handelDates(start: any, end: any): any {
  const dates = {
    start,
    end,
    add: true,
    cut: null,
    endStr: null as null | string | Date,
    startStr: null as null | string | Date
  }

  const endDate = new Date(dates.end || '')
  if (dates.cut) {
    endDate.setDate(endDate.getDate() - 1)
  } else if (dates.add) {
    endDate.setDate(endDate.getDate() + 1)
  }

  dates.end = endDate
  dates.start = new Date(dates.start)

  const endStr = `${endDate.getFullYear()}-${endDate.getMonth() + 1}-${endDate.getDate()}`
  const startStr = `${dates.start.getFullYear()}-${
    dates.start.getMonth() + 1
  }-${dates.start.getDate()}`

  dates.endStr = endStr
  dates.startStr = startStr
  return dates
}


export function normalizeEvent(e: Api.Event): any {
  const dates = handelDates(e.from_date, e.end_date)

  return {
    type: e.type,
    title: 'Event',
    classNames: ['cshr-event'],
    color: '#47a2ff',
    start: dates.start,
    end: dates.end,
    backgroundColor: '#47a2ff',
    id: e.type + e.id.toString(),
    allDay: true
  }
}
function formatTitle(v: Api.Vacation) {
  const fullName = v.applying_user_full_name ? v.applying_user_full_name : v.applying_user.full_name;
  const reason = v.reason.replace("_", " ").replace(/s$/, "");
  return `${fullName} ${reason}`;
}
export function normalizeVacation(v: Api.Vacation) {
  const dates = handelDates(v.from_date, v.end_date)

  return {
    type: v.type,
    title: formatTitle(v),
    color: '#fcd091',
    start: dates.start,
    end: dates.end,
    backgroundColor: '#fcd091',
    id: v.type + v.id.toString(),
    allDay: true
  }
}

export function normalizeHoliday(h: Api.Holiday) {
  const dates = handelDates(h.holiday_date, h.holiday_date)
  return {
    type: h.type,
    title: `Public Holiday ${h.location.country}`,
    color: '#5effb4',
    start: dates.start,
    end: dates.end,
    backgroundColor: '#5effb4',
    id: h.type + h.id.toString(),
    allDay: true
  }
}
export function normalizedBirthday(u: Api.User) {
  const dates = handelDates(u.date, u.date)

  return {
    type: u.type,
    title: `${u.full_name}'s Birthday`,
    color: '#e0adf0',
    start: dates.start,
    end: dates.end,
    backgroundColor: '#e0adf0',
    id: u.type + u.id.toString(),
    allDay: true
  }
}


export function normalizeMeeting(m: Api.Meeting): any {
  const dates = handelDates(m.date, m.date)

  return {
    type: m.type,
    title: 'Meeting',
    color: '#efeaea',
    start: dates.start,
    end: dates.end,
    backgroundColor: '#efeaea',
    id: m.type + m.id.toString(),
    allDay: true
  }
}
export function getStatusColor(status: Api.RequestStatus) {
  switch (status) {
    case 'pending':
      return 'yellow'
    case 'approved':
      return 'green'
    case 'rejected':
      return 'red'
    case 'canceled':
      return 'red'
    case 'requested_to_cancel':
      return 'orange'
    case 'cancel_approved':
      return 'green'
    case 'cancel_rejected':
      return 'red'
    default:
      return 'grey'
  }
}

export function formatRequestStatus(status: Api.RequestStatus) {
  return capitalize(status).replace('_', ' ').replace('_', ' ')
}

export function decodeAccessToken(token: string): JWTokenObject {
  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
  return JSON.parse(jsonPayload);
}

export function isValidToken(token: string): boolean {
  const decodedToken = decodeAccessToken(token);
  return Date.now() < decodedToken.exp * 1000;
}

export async function listUsers($api: ApiClient, page: number, count: number): Promise<{ page: number, count: number,  users: any[]}> {
  
    const res = await $api.users.admin.office_users.list({ page });
    const users: any[] = [];
    if (res.count) {
      count = Math.ceil(res.count / 10)
    } else {
      count = 0
    }
    res.results.forEach((user: any) => {
      users.push(user)
    })
    return { page, count, users };

}

export function convertToTimeOnly(datetime: string) {
  // Use a regular expression to capture the time part
  const match = datetime.match(/(?:T| )(\d{2}:\d{2})/);
  return match ? match[1] : '';
}

function timeStringToHours(time: string): number {
  const [hours, minutes] = time.split(':').map(Number);
  return hours + minutes / 60;
}

export function calculateTimes(excuseStart: string, excuseEnd: string) {
  const startTimeInHours = timeStringToHours(excuseStart);
  const endTimeInHours = timeStringToHours(excuseEnd);
  
  const CORE_HOURS = 8;
  const days = (endTimeInHours - startTimeInHours) / CORE_HOURS
  
  if (days <= .25) {
    return .25
  }

  if (days <= .5) {
    return .5
  }

  if (days <= .75) {
    return .75
  }
  
  return 1
}
