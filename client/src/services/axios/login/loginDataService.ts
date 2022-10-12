import http from "../http-common";
import type { loginDataType } from "./types";

class LoginDataService {
	async login(email: string, password: string) {
		const loginData: loginDataType = { email: email, password: password };

		try {
			return await (
				await http.post("auth/login/", loginData)
			).data.results;
		} catch (error) {
			throw new Error(error.response.data.detail);
		}
	}
}

const loginDataService = new LoginDataService();

export default loginDataService;
