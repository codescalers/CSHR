import axios from "axios";
import { authStore } from "../../stores";

const http = axios.create({
	baseURL: process.env.APP_BASE_API_URL +"api/",
	headers: {
		"Content-type": "application/json",
	},
});

http.interceptors.request.use((config) => {
	console.log("tab ana kedda barra el if bas b intercept");
	if (authStore.isAuth()) {
		console.log("howa ana delwa2ty b intercept");
		config.headers = {
			...config.headers,
			Authorization: `Bearer ${localStorage.getItem("accesstoken")}`,
		};
	}
	return config;
});

export default http;
