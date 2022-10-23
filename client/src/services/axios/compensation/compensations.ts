import type { CompensationType } from "../../../types";
import http from "../http-common";


class CompensationsDataService {
	errorMessage = "Error in Compensations Data Service: ";
	public async post(data: CompensationType) {
		try {
			return await http.post("/compensations/", data);
		} catch (err) {
			throw new Error(err.response.data.message);
		}
	}
	public async getByID(id: number) {
		try {
			return await http.get(`/compensations/${id}`);
		} catch (err) {
			throw new Error(err.response.data.message);
		}
	}
	public async delete(id: number) {
		try {
			return await http.delete(`/compensations/${id}`);
		} catch (err) {
			throw new Error(err.response.data.message);
		}
	}
}

const compensationsDataService = new CompensationsDataService();
export default compensationsDataService;
