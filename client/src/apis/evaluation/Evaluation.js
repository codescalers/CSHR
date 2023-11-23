import http from "../../utils/axios";
class EvaluationDataService {
    constructor() {
        this.errorMessage = "Error in Evaluation Data Service: ";
    }
    async allUserEvaluations() {
        try {
            const { data, status, statusText } = await http.get("/evaluation/users/");
            if (status !== 200) {
                throw new Error("Error in getting offices with status " + status + " wtih status text : " + statusText);
            }
            return data.results;
        }
        catch (err) {
            console.error(this.errorMessage + err);
        }
    }
    async UserEvaluations(id, year) {
        try {
            const { data, status, statusText } = await http.get(`/evaluation/user/${id}/?year=${year}`);
            if (status !== 200) {
                throw new Error("Error in getting offices with status " + status + " wtih status text : " + statusText);
            }
            return data.results;
        }
        catch (err) {
            console.error(this.errorMessage + err);
        }
    }
    async allEvaluations() {
        try {
            return await (await http.get(`/evaluation/`)).data;
        }
        catch (err) {
            console.error(this.errorMessage + err);
        }
    }
    async evaluationById(id) {
        try {
            return await (await http.get(`/evaluation/${id}/`)).data;
        }
        catch (err) {
            console.error(this.errorMessage + err);
        }
    }
    async postEvaluation(data) {
        try {
            await http.post("evaluation/", data);
        }
        catch (err) {
            console.error(this.errorMessage + err);
        }
    }
    async postUserEvaluation(data) {
        try {
            await http.post("evaluation/users/", data);
        }
        catch (err) {
            console.error(this.errorMessage + err);
        }
    }
}
const evaluationDataService = new EvaluationDataService();
export default evaluationDataService;
//# sourceMappingURL=Evaluation.js.map