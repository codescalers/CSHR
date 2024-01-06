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
  (v: string) => !!v || 'E-mmail is required.',
  (v: string) => /.+@.+/.test(v) || 'E-mail is not valid.'
]

export const passwordRules = [
  (v: string) => !!v || "Password is required.",
  (v: string) => v.length > 3 || "Password must be more than 3 characters."
]
