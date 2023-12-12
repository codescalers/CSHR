import http from "../../utils/axios";
import type {
  VacationBalanceAdjustmentType,
  VacationBalanceType
} from "../../utils/types";

class Vacation {
  errorMessage = "Error in Vacation Data Service: ";
  public async balance(userIDs: number[]) {
    try {
      const data = await http.get(`/vacations/balance/?user_ids=${userIDs}`);
      if (data.status === 404) {
        throw new Error("Balance not found");
      } else if (data.status !== 200) {
        throw new Error(data.data.message);
      }
      return data.data.results;
    } catch (error: any) {
      throw new Error(
        error.response.data.message || error.response.data.detail
      );
    }
  }

  public async vacatioDetails(id: number) {
    try {
      const data = await http.get(`/vacations/${id}/`);
      if (data.status === 404) {
        throw new Error("Vacation not found");
      } else if (data.status !== 200) {
        throw new Error(data.data.message);
      }
      return data.data.results;
    } catch (error: any) {
      throw new Error(error);
    }
  }

  public async comment(id: number, requestData: any) {
    try {
      const data = await http.put(`/vacations/comment/${id}/`, requestData);
      if (data.status === 404) {
        throw new Error("Vacation not found");
      } else if (data.status !== 202) {
        throw new Error(data.data.message);
      }
      return data.data.results;
    } catch (error: any) {
      throw new Error(error);
    }
  }

  public async calculator(startDate: string, endDate: string) {
    try {
      const data = await http.get(
        `/vacations/calculate/?start_date=${startDate}&end_date=${endDate}`
      );
      if (data.status === 404) {
        throw new Error("Actual days not found");
      } else if (data.status !== 200) {
        throw new Error(data.data.message);
      }
      return data.data.results;
    } catch (error: any) {
      throw new Error(
        error.response.data.message || error.response.data.detail
      );
    }
  }

  public async postAdminBalance(data: VacationBalanceType) {
    try {
      await http.post("vacations/post-admin-balance/", data);
    } catch (err: any) {
      throw new Error(err.response.data.message || err.response.data.detail);
    }
  }

  public async getAdminbalance() {
    try {
      return (await http.get("vacations/get-admin-balance/")).data.results;
    } catch (err: any) {
      throw new Error(err.response.data.message || err.response.data.detail);
    }
  }

  public async updateUserBalance(
    userBalance: VacationBalanceType,
    userIDs: number[]
  ) {
    try {
      return (
        await http.put(`/vacations/balance/?user_ids=${userIDs}`, userBalance)
      ).data.results;
    } catch (err: any) {
      throw new Error(err.response.data.message || err.response.data.detail);
    }
  }

  public async post(e: {
    applyingUserId: number;
    reason: string;
    end_date: string;
    from_date: string;
  }) {
    try {
      if (!e.applyingUserId || !e.end_date) throw new Error("Invalid data");
      const axios = await http.post(
        "/vacations/",
        JSON.stringify({
          applying_user: e.applyingUserId,
          from_date: e.from_date,
          end_date: e.end_date,
          reason: e.reason,
          type: "vacations",
          status: "pending"
        })
      );
      return axios;
    } catch (error: any) {
      this.errorMessage =
        error.response.data.message || error.response.data.detail;
      throw new Error(this.errorMessage);
    }
  }

  public async update(vacationID: string, data: any) {
    try {
      return await (
        await http.put(`/vacations/edit/${vacationID}/`, data)
      ).data;
    } catch (error: any) {
      this.errorMessage =
        error.response.data.message || error.response.data.detail;
      throw new Error(this.errorMessage);
    }
  }

  public async vacationBalanceAdjustment(
    payload: VacationBalanceAdjustmentType
  ) {
    try {
      return await (
        await http.put(`/vacations/balance/adjustment/`, payload)
      ).data;
    } catch (error: any) {
      this.errorMessage =
        error.response.data.message || error.response.data.detail;
      throw new Error(this.errorMessage);
    }
  }
}

const vacation = new Vacation();
export default vacation;
