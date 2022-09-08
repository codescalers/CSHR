import http from "../http-common";
class UserDataService {
    errorMessage: string = "Error in User Data Service: ";
    public async getAll() {
        try {
            return await (await http.get(`/users/`)).data;
        } catch (err) {
            console.log(this.errorMessage + err);
        }
    }
    public async getById(id: number) {
        try {
            return await (await http.get(`/users?id=${id}`)).data;
        } catch (err) {
            console.log(this.errorMessage + err);
        }
    }
}

const userDataService = new UserDataService();
export default userDataService;