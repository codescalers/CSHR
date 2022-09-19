import http from "../http-common";
class OfficeDataService {
    errorMessage: string = "Error in Office Data Service: ";
    public async getAll() {
        try {
            const { data, status, statusText } = await http.get(`/office/`);
            if (status !== 200) {
                throw new Error("Error in getting offices with status " + status + " wtih status text : " + statusText);
            }
            return data.results;
        } catch (err) {
            console.error(this.errorMessage + err);
            throw new Error(err);

        }
    }
    public async getById(id: number) {
        try {
            const { data, status, statusText } = await http.get(`/users?id=${id}`);
            if (status !== 200) {
                throw new Error("Error in getting offices with status " + status + " wtih status text : " + statusText);
            }
            return data;
        } catch (err) {
            console.error(this.errorMessage + err);
            throw new Error(err);
        }
    }
}

const officeDataService = new OfficeDataService();
export default officeDataService;