import moment from 'moment'

import type { Api } from "@/types"

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

export const fieldRequired = [(v: string) => !!v || 'Field is required.']

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


export function normalizeEvent(e: Api.Inputs.Event): any {
  const dates = handelDates(e.from_date, e.end_date)

  return {
    title: 'Event',
    classNames: ['cshr-event'],
    color: 'primary',
    start: dates.start,
    end: dates.end,
    backgroundColor: 'primary',
    id: e.name,
    allDay: true
  }
}
export function normalizeVacation(v: Api.Vacation) {
  const dates = handelDates(v.from_date, v.end_date)

  return {
    title: `${v.user!.full_name}'s Vacation`,
    color: 'primary',
    start: dates.start,
    end: dates.end,
    backgroundColor: 'gray',
    id: v.id.toString(),
    allDay: true
  }
}

export function normalizeHoliday(h: Api.Holiday) {
  const dates = handelDates(h.holiday_date, h.holiday_date)

  return {
    title: `PublicVacation`,
    color: 'primary',
    start: dates.start,
    end: dates.end,
    backgroundColor: 'gray',
    id: h.id.toString(),
    allDay: true
  }
}


export function normalizeMeeting(m: Api.Meetings): any {
  const dates = handelDates(m.date, m.date)

  return {
    title: 'Meeting',
    color: 'secondary',
    start: dates.start,
    end: dates.end,
    backgroundColor: 'primary',
    id: m.id,
    allDay: true
  }
}