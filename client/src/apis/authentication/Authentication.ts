import type { loginDataType, refreshData } from "../../utils/types";
import httpAxios from "../../utils/axios";

class Authentication{
	async refresh(refresh: string): Promise<refreshData> {
		// Request for getting a refresh token when token expires.
		try {
			return (await httpAxios.post("/auth/token/refresh/", { refresh: refresh })).data
		} catch (error) {
			throw new Error(error);
		}
	}

	async login(email: string, password: string) {
		// Request for getting an access token to user with his credentials.
		const loginData: loginDataType = { email: email, password: password };		
		try {
			return await (
				await httpAxios.post("auth/login/", loginData)
			).data;
		} catch (error) {
			throw new Error(error.response.data.detail || error.response.data.message);
		}
	}
}

const authenticationAPI = new Authentication();
export default authenticationAPI;
