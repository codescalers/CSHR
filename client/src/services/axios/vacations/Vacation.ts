import type { VacationBalanceType } from "../../../types";
import http from "../http-common";


class Vacation{
	errorMessage = "Error in Vacation Data Service: ";
	public async balance(userID: number) {
		try {
			const data = await http.get(`/vacations/balance/?user_id=${userID}`);
			if (data.status === 404) {
				throw new Error("Balance not found");
			} else if (data.status !== 200) {
				throw new Error(data.data.message);
			}
			return data.data.results;
		} catch (error) {
			throw new Error(error.response.data.message);
		}
	}
	public async vacatioDetails(id : number) {
		try {
			const data = await http.get(`/vacations/${id}/`);
			if (data.status === 404) {
				throw new Error("Vacation not found");
			} else if (data.status !== 200) {
				throw new Error(data.data.message);
			}
			return data.data.results;
		} catch (error) {
			throw new Error(error);
		}
	}
	public async comment(id : number, requestData: any) {
		try {
			const data = await http.put(`/vacations/comment/${id}/`, requestData);
			if (data.status === 404) {
				throw new Error("Vacation not found");
			} else if (data.status !== 202) {
				throw new Error(data.data.message);
			}
			return data.data.results;
		} catch (error) {
			throw new Error(error);
		}
	}
	public async calculator(startDate: string, endDate: string) {
		try {
			const data = await http.get(`/vacations/calculate/?start_date=${startDate}&end_date=${endDate}`);
			if (data.status === 404) {
				throw new Error("Actual days not found");
			} else if (data.status !== 200) {
				throw new Error(data.data.message);
			}
			return data.data.results;
		} catch (error) {
			throw new Error(error);
		}
	}
	public async postAdminBalance(data: {
		annual_leaves: number;
		emergency_leaves: number;
		leave_excuses: number;
		public_holidays: string[];
	}) {
		try {
			await http.post("vacations/admin-balance/", data);
		} catch (err) {
			throw new Error(err.response.data.message);
		}
	}
	public async updateUserBalance(userBalance: VacationBalanceType) {
		try {
			await http.put(`/vacations/balance/?user_id=${userBalance.user.id}`, userBalance);
		} catch (err) {
			throw new Error(err.response.data.message);
		}
	}
}

const vacation = new Vacation();
export default vacation;