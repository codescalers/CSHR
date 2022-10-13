import axios from "axios";
import { authStore } from "../../stores";

const http = axios.create({
	baseURL: process.env.APP_BASE_API_URL + "api/",
	headers: {
		"Content-type": "application/json",
	},
});

http.interceptors.request.use((config) => {
	if (authStore.isAuth()) {
		config.headers = {
			...config.headers,
			Authorization: `Bearer ${localStorage.getItem("accesstoken")}`,
		};
	}
	return config;
});

export default http;
