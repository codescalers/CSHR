import http from "../../utils/axios";
import type { CompensationType } from "../../utils/types";

class CompensationsDataService {
  public async post(data: CompensationType) {
    // Request to post user compensations
    try {
      return await http.post("/compensations/", data);
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }

  public async update(data: JSON | object, id: number) {
    // Request to update user compensations
    try {
      return await http.put(`compensations/edit/${id}/`, data);
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }

  public async getByID(id: number) {
    // Request to get compensation by id
    try {
      return await http.get(`/compensations/${id}`);
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }

  public async delete(id: number) {
    // Request to delete user compensations
    try {
      return await http.delete(`/compensations/${id}`);
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }

  public async userCompensations() {
    // Request to get all user compensations
    try {
      return await http.get(`/compensations/user`);
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }
}

const compensationsDataService = new CompensationsDataService();
export default compensationsDataService;
