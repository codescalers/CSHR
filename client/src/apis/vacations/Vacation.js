import http from "../../utils/axios";
class Vacation {
    constructor() {
        this.errorMessage = "Error in Vacation Data Service: ";
    }
    async balance(userID) {
        try {
            const data = await http.get(`/vacations/balance/?user_id=${userID}`);
            if (data.status === 404) {
                throw new Error("Balance not found");
            }
            else if (data.status !== 200) {
                throw new Error(data.data.message);
            }
            return data.data.results;
        }
        catch (error) {
            throw new Error(error.response.data.message || error.response.data.detail);
        }
    }
    async vacatioDetails(id) {
        try {
            const data = await http.get(`/vacations/${id}/`);
            if (data.status === 404) {
                throw new Error("Vacation not found");
            }
            else if (data.status !== 200) {
                throw new Error(data.data.message);
            }
            return data.data.results;
        }
        catch (error) {
            throw new Error(error);
        }
    }
    async comment(id, requestData) {
        try {
            const data = await http.put(`/vacations/comment/${id}/`, requestData);
            if (data.status === 404) {
                throw new Error("Vacation not found");
            }
            else if (data.status !== 202) {
                throw new Error(data.data.message);
            }
            return data.data.results;
        }
        catch (error) {
            throw new Error(error);
        }
    }
    async calculator(startDate, endDate) {
        try {
            const data = await http.get(`/vacations/calculate/?start_date=${startDate}&end_date=${endDate}`);
            if (data.status === 404) {
                throw new Error("Actual days not found");
            }
            else if (data.status !== 200) {
                throw new Error(data.data.message);
            }
            return data.data.results;
        }
        catch (error) {
            throw new Error(error.response.data.message || error.response.data.detail);
        }
    }
    async postAdminBalance(data) {
        try {
            await http.post("vacations/post-admin-balance/", data);
        }
        catch (err) {
            throw new Error(err.response.data.message || err.response.data.detail);
        }
    }
    async getAdminbalance() {
        try {
            return (await http.get("vacations/get-admin-balance/")).data.results;
        }
        catch (err) {
            throw new Error(err.response.data.message || err.response.data.detail);
        }
    }
    async updateUserBalance(userBalance) {
        try {
            await http.put(`/vacations/balance/?user_id=${userBalance.user.id}`, userBalance);
        }
        catch (err) {
            throw new Error(err.response.data.message || err.response.data.detail);
        }
    }
    async post(e) {
        try {
            if (!e.applyingUserId || !e.end_date)
                throw new Error("Invalid data");
            const axios = await http.post("/vacations/", JSON.stringify({
                applying_user: e.applyingUserId,
                from_date: e.from_date,
                end_date: e.end_date,
                reason: e.reason,
                type: "vacations",
                status: "pending",
            }));
            return axios;
        }
        catch (error) {
            this.errorMessage = error.response.data.message || error.response.data.detail;
            throw new Error(this.errorMessage);
        }
    }
    async update(vacationID, data) {
        try {
            return await (await http.put(`/vacations/edit/${vacationID}/`, data)).data;
        }
        catch (error) {
            this.errorMessage = error.response.data.message || error.response.data.detail;
            throw new Error(this.errorMessage);
        }
    }
}
const vacation = new Vacation();
export default vacation;
//# sourceMappingURL=Vacation.js.map