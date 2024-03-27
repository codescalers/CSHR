import axios from 'axios'

import { ApiClient } from './api'

console.log(`Connected on server: ${window.env.SERVER_DOMAIN_NAME_API}`);
const accessToken = localStorage.getItem("access_token")

export const $api = new ApiClient({
  $http: axios.create({
    baseURL: window.env.SERVER_DOMAIN_NAME_API,
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  }),
});