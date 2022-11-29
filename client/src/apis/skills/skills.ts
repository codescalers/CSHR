
import type { UserInterface } from "../../utils/types";
import http from "../../utils/axios";

class SkillsDataService {
	errorMessage = "Error in Skills Data Service:  with status ";
	public async getAll() {
		try {
			const { data, status, statusText } = await http.get("/users/skills/");
			if (status === 404) {
				throw new Error("Skills not found");
			} else if (status !== 200) {
				throw new Error(
					this.errorMessage + status + " wtih status text : " + statusText
				);
			};
			return data.results;
		} catch (error) {
			throw new Error(error);
		};
	};
	async postSkills(user: UserInterface, skills: string[]){
		try {
			return await (
				await http.post("/users/skills/add_skill/", JSON.stringify({"user_id": user.id, "skills": skills}))
			).data;
		} catch (error) {
			throw new Error(`Error while registering${error}`);
		}
	}
};

const skillsDataService = new SkillsDataService();
export default skillsDataService;
