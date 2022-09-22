import http from "../http-common";

export default async function updateCompensation(
	id: string,
	data: JSON | Object
) {
	const response = await await http.put(`compensation/edit/${id}/`, data);
	if (response.status == 202) {
		return true;
	}
}
