import http from "../http-common";


class RequestTypes {
	errorMessage = "Error in Office Data Service: ";
	public async approve(incomingData: Object | JSON, id: number) {
		console.log(id);
		try {
			const { data, status, statusText } = await http.put(`/requests/approve/${id}/`, incomingData);
			if (status !== 202) {
				throw new Error(
					"Error in getting offices with status " +
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

const requestTypes = new RequestTypes();
export default requestTypes;

// export default async function updateCompensation(
// 	id: string,
// 	data: JSON | Object
// ) {
// 	const response = await await http.put(`compensation/edit/${id}/`, data);
// 	if (response.status == 202) {
// 		return true;
// 	}
// }
