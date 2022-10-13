import type { PaginatedInterface, SupervisorType, TeamType } from "./../../../types";
import http from "../http-common";

class TeamDataService {
	errorMessage = "Error in Team Data Service: ";
	public async getTeams(): Promise<PaginatedInterface<TeamType>> {
		try {
			const { data, status, statusText } = await http.get("/users/teams/");
			if (status !== 200) {
				throw new Error(
					"Error in getting team with status " +
            status +
            " wtih status text : " +
            statusText
				);
			}
			const { results, next, previous, count } = data;
			return { results, next, previous, count };
		} catch (err) {
			console.error(this.errorMessage + err);
			throw new Error(err);
		}
	}
	public async getSupervisor(): Promise<PaginatedInterface<SupervisorType>> {
		try {
			const { data, status, statusText } = await http.get("/users/teams/supervisors/");
			if (status !== 200) {
				throw new Error(
					"Error in getting team with status " +
            status +
            " wtih status text : " +
            statusText
				);
			}
			const { results, next, previous, count } = data;
			return { results, next, previous, count };
		} catch (err) {
			console.error(this.errorMessage + err);
			throw new Error(err);
		}
	}
}

const teamDataService = new TeamDataService();
export default teamDataService;
