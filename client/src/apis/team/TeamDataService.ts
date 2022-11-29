import type { PaginatedInterface, SupervisorType, TeamType } from "../../utils/types";
import http from "../../utils/axios";

class TeamDataService {
	errorMessage = "Error in Team Data Service: ";
	public async getTeams(){
		try {
			return await http.get("/users/teams/");
		} catch (err) {
			throw new Error(err.response.data.message);
		}
	}
	public async getSupervisor(){
		try {
			return await http.get("/users/teams/supervisors/");
		} catch (err) {
			throw new Error(err.response.data.message);
		}
	}
}

const teamDataService = new TeamDataService();
export default teamDataService;
