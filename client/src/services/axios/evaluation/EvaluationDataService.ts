import http from "../http-common";
class EvaluationDataService {
	errorMessage = "Error in Evaluation Data Service: ";
	public async getByAll() {
		try {
			const { data, status, statusText } = await http.get("/evaluation/user/");
			if (status !== 200) {
				throw new Error(
					"Error in getting offices with status " +
            status +
            " wtih status text : " +
            statusText
				);
			}
			console.log(data)
			return data.results;
		} catch (err) {
			console.error(this.errorMessage + err);
		}
	}
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
			await http.post("evaluation/", data);
		} catch (err) {
			console.error(this.errorMessage + err);
		}
	}
}

const evaluationDataService = new EvaluationDataService();
export default evaluationDataService;
