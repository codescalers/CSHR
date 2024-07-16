import { test_auth_api } from './auth'

export async function test_api() {
  const { loggedUser, user, refresh, c1, c2 } = await test_auth_api()
  return { loggedUser, user, refresh, c1, c2 }
}
