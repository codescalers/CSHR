import http from "../../utils/axios";

class OfficeDataService {
  // Class office service to serve all office endpoints.
  errorMessage = "Error in Office Data Service: ";
  public async getAll() {
    try {
      const { data, status, statusText } = await http.get("/office/");
      if (status !== 200) {
        throw new Error("Error in getting offices with status " + status + " wtih status text : " + statusText);
      }
      return data.results;
    } catch (err: any) {
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
    } catch (err: any) {
      console.error(this.errorMessage + err);
      throw new Error(err);
    }
  }
  public async post(data: { name: string; country: string; weekend: string }) {
    try {
      await http.post("/office/", data);
    } catch (err: any) {
      console.error(this.errorMessage + err);
    }
  }
}

const officeDataService = new OfficeDataService();
export default officeDataService;
