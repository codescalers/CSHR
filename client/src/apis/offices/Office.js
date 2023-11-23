import http from "../../utils/axios";
class OfficeDataService {
    constructor() {
        // Class office service to serve all office endpoints.
        this.errorMessage = "Error in Office Data Service: ";
    }
    async getAll() {
        try {
            const { data, status, statusText } = await http.get("/office/");
            if (status !== 200) {
                throw new Error("Error in getting offices with status " + status + " wtih status text : " + statusText);
            }
            return data.results;
        }
        catch (err) {
            console.error(this.errorMessage + err);
            throw new Error(err);
        }
    }
    async getById(id) {
        try {
            const { data, status, statusText } = await http.get(`/users?id=${id}`);
            if (status !== 200) {
                throw new Error("Error in getting offices with status " + status + " wtih status text : " + statusText);
            }
            return data;
        }
        catch (err) {
            console.error(this.errorMessage + err);
            throw new Error(err);
        }
    }
    async post(data) {
        try {
            await http.post("/office/", data);
        }
        catch (err) {
            console.error(this.errorMessage + err);
        }
    }
}
const officeDataService = new OfficeDataService();
export default officeDataService;
//# sourceMappingURL=Office.js.map