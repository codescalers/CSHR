import { faker } from '@faker-js/faker'

import { $api } from '@/clients'

export async function test_auth_api(password = '1') {
  const loggedUser = await $api.auth.login({ email: 'admin@admin.tf', password })

  const user = await $api.auth.register({
    first_name: faker.person.firstName(),
    last_name: faker.person.lastName(),
    address: faker.location.streetAddress(),
    birthday: `1997-12-14`,
    email: faker.internet.email(),
    gender: 'Male',
    job_title: 'Senior Developer',
    joining_at: `2024-01-01`,
    location: 1,
    mobile_number: faker.phone.number().slice(0, 11),
    password: '1',
    social_insurance_number: '123456789',
    team: 'Development',
    telegram_link: '@name',
    user_type: 'Admin',
    salary: {},
    reporting_to: [1]
  })

  const refresh = await $api.auth.refresh({ refresh: loggedUser.refresh_token })

  const newPassword = password === '1' ? '0' : '1'

  const c1 = await $api.auth.changePassword({ old_password: password, new_password: newPassword })

  const c2 = await $api.auth.changePassword({ old_password: newPassword, new_password: password })

  return { loggedUser, user, refresh, c1, c2 }
}
