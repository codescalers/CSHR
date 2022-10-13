import http from "../http-common";

class Requests {
	errorMessage = "Error in Request Data Service: ";
	public async getRequests() {
		const data = (await http.get("requests/")).data.results;
		const request: any = [];
	
		data.vacations.forEach(function (value: any) {
			value.type = "Vacation";
			request.push(value);
		});
	
		data.hr_letters.forEach(function (value: any) {
			value.type = "HR letters";
			request.push(value);
		});
	
		document.body.style.cursor = "default";
		return request;
	}

	public async approve(incomingData: Object | JSON, id: number) {
		try {
			const { data, status, statusText } = await http.put(`/vacations/approve/${id}/`, incomingData);
			if (status !== 202) {
				throw new Error(
					"Error while approving this request." +
            status +
            " wtih status text : " +
            statusText
				);
			}
			return data.results;
		} catch (err) {
			console.error(this.errorMessage + err);
			throw new Error(err);
		}
	}

	public async reject(incomingData: Object | JSON, id: number) {
		try {
			const { data, status, statusText } = await http.put(`/vacations/reject/${id}/`, incomingData);
			if (status !== 202) {
				throw new Error(
					"Error while approving this request." +
            status +
            " wtih status text : " +
            statusText
				);
			}
			return data.results;
		} catch (err) {
			console.error(this.errorMessage + err);
			throw new Error(err);
		}
	}
}

const requestTypes = new Requests();
export default requestTypes;