import axios from "axios";

import { authStore } from "./stores";

console.log("Connected to server on: ", window.configs.SERVER_BASE_URL);

if (!window.configs.SERVER_API_URL) {
  throw new Error(
    `Invalid config. Please fill the config.json file with the correct data`
  );
}

const http = axios.create({
  baseURL: window.configs.SERVER_API_URL,
  headers: {
    "Content-Type": "application/json"
  }
});

http.interceptors.request.use((config) => {
  if (authStore.isAuth()) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${localStorage.getItem("accesstoken")}`
    };
  }
  return config;
});

export default http;
