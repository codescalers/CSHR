import type { HRLetterType } from "../../../types";
import http from "../http-common";


class HRLetterDataService {
	public async post(data: HRLetterType) {
		try {
			return await http.post("/hr_letters/", data);
		} catch (err) {
			throw new Error(err.response.data.message);
		}
	}
	public async postOfficialDocument(data: any) {
		try {
			return await http.post("/official_documents/", data);
		} catch (err) {
			throw new Error(err.response.data.message);
		}
	}
	public async getByID(id: number) {
		try {
			return await http.get(`/hr_letters/${id}/`);
		} catch (err) {
			throw new Error(err.response.data.message);
		}
	}
}

const hrLetterDataService = new HRLetterDataService();
export default hrLetterDataService;
