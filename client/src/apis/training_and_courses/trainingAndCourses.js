import http from "../../utils/axios";
class TrainingAndCourses {
    constructor() {
        this.errorMessage = "Error in training and courses Data Service:  with status ";
    }
    async post(data) {
        try {
            return await (await http.post("/training_courses/", data)).data;
        }
        catch (error) {
            throw new Error(`Error while registering${error}`);
        }
    }
}
const trainingAndCourses = new TrainingAndCourses();
export default trainingAndCourses;
//# sourceMappingURL=trainingAndCourses.js.map