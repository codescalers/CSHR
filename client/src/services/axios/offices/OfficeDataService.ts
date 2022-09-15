import http from "../http-common";
class OfficeDataService {
    errorMessage: string = "Error in Office Data Service: ";
    public async getAll() {
        try {
            return await (await http.get(`/office/`)).data;
        } catch (err) {
            console.error(this.errorMessage + err);
        }
    }
    public async getById(id: number) {
        try {
            return await (await http.get(`/users?id=${id}`)).data;
        } catch (err) {
            console.error(this.errorMessage + err);
        }
    }
}

const officeDataService = new OfficeDataService();
export default officeDataService;