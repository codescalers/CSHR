import http from "../http-common";

export default async function getRequests() {
	const data = (await http.get("requests/")).data.data;
	const request = [];

	data.vacations.forEach(function (value) {
		value.type = "Vacation";
		request.push(value);
	});
	data.compensations.forEach(function (value) {
		value.type = "Compensation";
		request.push(value);
	});
	data.hr_letters.forEach(function (value) {
		value.type = "HR letters";
		request.push(value);
	});
	document.body.style.cursor = "default";
	return request;
}
