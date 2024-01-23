import axios from 'axios'

import { ApiClient } from './api'

export const $api = new ApiClient({
  $http: axios.create({
    baseURL: window.env.CSHR_API
  })
})
