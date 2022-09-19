import http from "../http-common";
class UsersDataService {
    errorMessage: string = "Error in User Data Service: ";
    public async getAll() {
        try {
            const { data, status, statusText } = (await http.get(`/users/`));

            if (status !== 200) {
                throw new Error("Error in getting users with status " + status + " wtih status text : " + statusText);
            }
            return data.results;

        } catch (err) {
            console.error(this.errorMessage + err);
            throw new Error(err);

        }
    }
    public async getById(id: number) {
        try {
            return await (await http.get(`/users?id=${id}`)).data;
        } catch (err) {
            console.error(this.errorMessage + err);
            throw new Error(err);
        }
    }
}

const usersDataService = new UsersDataService();
export default usersDataService;