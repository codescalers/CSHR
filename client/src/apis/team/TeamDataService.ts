import http from "../../utils/axios";
// import type { PaginatedInterface, TeamLeadType, TeamType } from "../../utils/types";

class TeamDataService {
  errorMessage = "Error in Team Data Service: ";
  public async getTeams() {
    try {
      return await http.get("/users/team/");
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }
  public async getTeamLead() {
    try {
      return await http.get("/users/team/team_leads/");
    } catch (err: any) {
      throw new Error(err.response.data.message);
    }
  }
}

const teamDataService = new TeamDataService();
export default teamDataService;
