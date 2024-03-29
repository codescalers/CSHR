import http from "../../utils/axios";

class TrainingAndCourses {
  errorMessage = "Error in training and courses Data Service:  with status ";

  async post(data: {
    name: string;
    certificate_link: string;
    user_id: number;
  }) {
    try {
      return await (
        await http.post("/training_courses/", data)
      ).data;
    } catch (error: any) {
      throw new Error(`Error while registering${error}`);
    }
  }
}

const trainingAndCourses = new TrainingAndCourses();
export default trainingAndCourses;
