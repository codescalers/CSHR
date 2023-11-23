import http from "../../utils/axios";
import type { HRLetterType } from "../../utils/types";

class HRLetterDataService {
  public async post(data: HRLetterType) {
    try {
      return await http.post("/hr_letters/", data);
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }
  public async postOfficialDocument(data: any) {
    try {
      return await http.post("/official_documents/", data);
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }
  public async getByID(id: number) {
    try {
      return await http.get(`/hr_letters/${id}/`);
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }
}

const hrLetterDataService = new HRLetterDataService();
export default hrLetterDataService;
