import http from "../http-common";
class EvaluationDataService {
	errorMessage = "Error in Evaluation Data Service: ";
	public async allUserEvaluations() {
		try {
			const { data, status, statusText } = await http.get("/evaluation/users/");
			if (status !== 200) {
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
		}
	}
	public async UserEvaluations(id: number, year: number) {
		try {
			const { data, status, statusText } = await http.get(`/evaluation/user/${id}/?year=${year}`);
			if (status !== 200) {
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
		}
	}
	public async allEvaluations() {
		try {
			return await (
				await http.get(`/evaluation/`)
			).data;
		} catch (err) {
			console.error(this.errorMessage + err);
		}
	}
	public async evaluationById(id: number) {
		try {
			return await (
				await http.get(`/evaluation/${id}/`)
			).data;
		} catch (err) {
			console.error(this.errorMessage + err);
		}
	}

	public async postEvaluation(data: {
		form: string;
		quarter: string;
		link: string;
	}) {
		try {
			await http.post("evaluation/", data);
		} catch (err) {
			console.error(this.errorMessage + err);
		}
	}
	public async postUserEvaluation(data: {
		user: number;
		quarter: string;
		link: string;
		score: number;
	}) {
		try {
			await http.post("evaluation/users/", data);
		} catch (err) {
			console.error(this.errorMessage + err);
		}
	}
}

const evaluationDataService = new EvaluationDataService();
export default evaluationDataService;
