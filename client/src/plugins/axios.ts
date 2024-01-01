import axios from 'axios'

export function createHttp() {
  return axios.create({
    baseURL: import.meta.env.VITE_CSHR_API
  })
}
