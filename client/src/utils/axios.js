import axios from "axios";
import { authStore } from "./stores";
if (!window.configs.SERVER_API_URL) {
    throw new Error(`Invalid config. Please fill the config.json file with the correct data`);
}
const http = axios.create({
    baseURL: window.configs.SERVER_API_URL,
    headers: {
        "Content-Type": "application/json",
    },
});
http.interceptors.request.use(config => {
    if (authStore.isAuth()) {
        config.headers = Object.assign(Object.assign({}, config.headers), { Authorization: `Bearer ${localStorage.getItem("accesstoken")}` });
    }
    return config;
});
export default http;
//# sourceMappingURL=axios.js.map