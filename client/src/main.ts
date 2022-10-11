import type { AxiosResponse } from "axios";
import App from "./App.svelte";

const app = new App({
	target: document.body,
});

export default app;

export const IsAuthenticated = (response: AxiosResponse) => {
	console.log("response",response);
	if (response.response.status == 403){
		window.location.href = '/login';
	}
}