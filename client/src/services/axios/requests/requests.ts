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
		
		data.compensations.forEach(function (value: any) {
			value.type = "Compensations";
			request.push(value);
		});
	
		document.body.style.cursor = "default";
		return request;
	}

	public async approve(incomingData: any, id: number) {
		console.log(incomingData);
		try {
			const { data, status, statusText } = await http.put(`/${incomingData.type.toLowerCase()}/approve/${id}/`, incomingData);
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
			throw new Error(err.response.data.message);
		}
	}

	public async reject(incomingData: any, id: number) {
		try {
			const { data, status, statusText } = await http.put(`/${incomingData.type.toLowerCase()}/reject/${id}/`, incomingData);
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
			throw new Error(err.response.data.message);
		}
	}
	public async delete(incomingData: any) {
		try {
			const { data, status, statusText } = await http.delete(`/${incomingData.type.toLowerCase()}/${incomingData.id}/`);
			if (status !== 204) {
				throw new Error(
					"Error while approving this request." +
            status +
            " wtih status text : " +
            statusText
				);
			}
			return data.results;
		} catch (err) {
			throw new Error(err.response.data.message);
		}
	}
}

const requestTypes = new Requests();
export default requestTypes;