import http from "../http-common";

class RefreshDataService {
	async refresh(refresh: string) {
		try {
			return await (
				await http.post("/auth/token/refresh/", { refresh: refresh })
			).data;
		} catch (error) {
			throw new Error(`Error to refresh token ${error}`);
		}
	}
}

const refreshDataService = new RefreshDataService();

export default refreshDataService;
