import http from "../http-common";


class Vacation{
	errorMessage = "Error in Vacation Data Service: ";
	public async balance() {
		try {
			const data = await http.get("/vacations/balance/");
			if (data.status === 404) {
				throw new Error("Balance not found");
			} else if (data.status !== 200) {
				throw new Error(data.data.message);
			}
			return data.data.results;
		} catch (error) {
			throw new Error(error);
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
		leave_execuses: number;
		public_holidays: string[];
	}) {
		try {
			await http.post("vacations/admin-balance/", data);
		} catch (err) {
			console.error(this.errorMessage + err);
		}
	}
}

const vacation = new Vacation();
export default vacation;