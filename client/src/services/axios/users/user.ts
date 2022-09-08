import http from "../http-common";
class UserDataService {

    public async getAll(): Promise<{ data: any[] }> {
        return http.get(`/users`);
    }
    public async getById(id: number): Promise<{ data: any[] }> {
        return http.get(`/users?id=${id}`);
    }


}

export default new UserDataService();