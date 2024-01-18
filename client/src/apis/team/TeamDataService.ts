import http from "../../utils/axios";
// import type { PaginatedInterface, SupervisorType, TeamType } from "../../utils/types";

class TeamDataService {
  errorMessage = "Error in Team Data Service: ";
  public async getTeams() {
    try {
      return await http.get("/users/team/");
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }
  public async getSupervisor() {
    try {
      return await http.get("/users/team/supervisors/");
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }
}

const teamDataService = new TeamDataService();
export default teamDataService;
