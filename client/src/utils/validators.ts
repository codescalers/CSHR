export const nameRules = [
  (v: string) => typeof v === 'string' || 'Name must be a string.',
  (v: string) => !!v || 'Name is required.',
  (v: string) =>
    (v && v.length >= 3 && v.length <= 50) || 'Name must be between 3 and 50 characters.'
]

export const emailRules = [
  (v: string) => typeof v === 'string' || 'Email must be a string.',
  (v: string) => !!v || 'Email is required.',
  (v: string) => /.+@.+\..+/.test(v) || 'Email is not valid.'
]

export const passwordRules = [
  (v: string) => typeof v === 'string' || 'Password must be a string.',
  (v: string) => !!v || 'Password is required.',
  (v: string) =>
    (v && v.length >= 4 && v.length <= 20) || 'Password must be between 4 and 20 characters.'
]

export const mobileRules = [
  (v: string) => typeof +v === 'number' || 'Mobile Number must be a number.',
  (v: string) => !!v || 'Mobile Number is required.',
  (v: string) =>
    (v && v.toString().length >= 10 && v.toString().length <= 15) || 'Enter a valid mobile number.'
]

export const jobRules = [
  (v: string) => typeof v === 'string' || 'Role must be a string.',
  (v: string) => !!v || 'Role is required.',
  (v: string) =>
    (v && v.length >= 3 && v.length <= 50) || 'Role must be between 3 and 50 characters.'
]

export const addressRules = [
  (v: string) => typeof v === 'string' || 'Address must be a string.',
  (v: string) => !!v || 'Address is required.',
  (v: string) =>
    (v && v.length >= 3 && v.length <= 50) || 'Address must be between 3 and 50 characters.'
]
export const socialInsuranceRules = [
  (v: string) => typeof v === 'string' || 'Social Number must be a string.',
  (v: string) => !!v || 'Social Number is required.',
  (v: string) =>
    (v && v.length >= 3 && v.length <= 50) || 'Social Number must be between 3 and 50 characters.'
]
export const telegramRules = [
  (v: string) => typeof v === 'string' || 'Telegram must be a string.',
  (v: string) => !!v || 'Telegram is required.',
  (v: string) => /^@([A-Za-z0-9_]{1,255})$/.test(v) || 'Telegram handle is not valid.',
  (v: string) =>
    (v && v.length >= 3 && v.length <= 50) || 'Telegram must be between 3 and 50 characters.'
]
export const requiredStringRules = [
  (v: string) => typeof v === 'string' || 'This field must be a string.',
  (v: string) => !!v || 'This field is required.'
]
export const requiredRules = [(v: string) => !!v || 'This field is required.']
export const vacationRules = [
  (v: string) => !!v || 'This field is required.',
  (v: string) => +v >= 0 || 'The minimum allowed value is 0. ',
  (v: string) => +v <= 80 || 'The maximum allowed value is 80. '
]
