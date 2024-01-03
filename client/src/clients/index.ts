import axios from 'axios'

import { ApiClient } from './api'

export const $api = new ApiClient({
  $http: axios.create({
    baseURL: import.meta.env.VITE_CSHR_API
  })
})