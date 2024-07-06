import axios from 'axios'

import { ApiClient } from './api'

console.log(`API connected on: ${window.env.SERVER_DOMAIN_NAME_API}`);
console.log(`WS connected on: ${window.env.SERVER_DOMAIN_NAME_WS}`);

const accessToken = localStorage.getItem("access_token")
export const $api = new ApiClient({
  $http: axios.create({
    baseURL: window.env.SERVER_DOMAIN_NAME_API,
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  }),
});