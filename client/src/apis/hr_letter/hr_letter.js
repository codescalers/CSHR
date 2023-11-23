import http from "../../utils/axios";
class HRLetterDataService {
    async post(data) {
        try {
            return await http.post("/hr_letters/", data);
        }
        catch (err) {
            throw new Error(err.response.data.message);
        }
    }
    async postOfficialDocument(data) {
        try {
            return await http.post("/official_documents/", data);
        }
        catch (err) {
            throw new Error(err.response.data.message);
        }
    }
    async getByID(id) {
        try {
            return await http.get(`/hr_letters/${id}/`);
        }
        catch (err) {
            throw new Error(err.response.data.message);
        }
    }
}
const hrLetterDataService = new HRLetterDataService();
export default hrLetterDataService;
//# sourceMappingURL=hr_letter.js.map