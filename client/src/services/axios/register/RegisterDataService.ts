import http from "../http-common";
import type { registeringData } from "./types";

class LoginDataService {
	async register(registerData: registeringData) {
		try {
			return await (
				await http.post("/auth/signup/", JSON.stringify(registerData))
			).data;
		} catch (error) {
			throw new Error(`Error while registering${error}`);
		}
	}
}

const loginDataService = new LoginDataService();

export default loginDataService;

