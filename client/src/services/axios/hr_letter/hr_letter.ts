import type { HRLetterType } from "../../../types";
import http from "../http-common";


class HRLetterDataService {
	errorMessage = "Error in Hr Letter Data Service: ";
	public async post(data: HRLetterType) {
		try {
			return await http.post("/hr_letters/", data);
		} catch (err) {
			throw new Error(err.response.data.message);
		}
	}
}

const hrLetterDataService = new HRLetterDataService();
export default hrLetterDataService;
