import http from "./http-common";
import type { TodoType } from "../../types";
class UserDataService {

    public async getAll(): Promise<{ data: TodoType[] }> {
        return http.get(`/users`);
    }
    public async getById(id: number): Promise<{ data: TodoType[] }> {
        return http.get(`/users?id=${id}`);
    }


}

export default new UserDataService();