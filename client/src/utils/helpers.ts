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

export const emailRules = [
  (v: string) => !!v || 'E-mail is required.',
  (v: string) => /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/.test(v) || 'E-mail is not valid.'
]

export const passwordRules = [
  (v: string) => !!v || 'Password is required.',
  (v: string) => v.length > 3 || 'Password must be more than 3 characters.'
]

export const DASHBOARD_ITEMS = [
  { id: 1, name: 'Set Vactions' },
  { id: 2, name: 'Set User Vacations' },
  { id: 3, name: 'Update Office Vacations' },
  { id: 4, name: 'Add Office' },
  { id: 5, name: 'Add User' },
  { id: 6, name: 'Update User Profile' },
]
