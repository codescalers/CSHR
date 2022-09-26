import http from "../http-common";
class EvaluationDataService {
	errorMessage = "Error in Evaluation Data Service: ";
	public async getById(id: number) {
		try {
			return await (
				await http.get(`/evaluation?id=${id}`)
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
			await http.post("evaluation/user/", data);
		} catch (err) {
			console.error(this.errorMessage + err);
		}
	}
}

const evaluationDataService = new EvaluationDataService();
export default evaluationDataService;
