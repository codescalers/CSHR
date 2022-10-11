import http from "../http-common";


class Vacation{
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
}

const vacation = new Vacation();
export default vacation;
