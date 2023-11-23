import http from "../../utils/axios";
// import type { PaginatedInterface, SupervisorType, TeamType } from "../../utils/types";
class TeamDataService {
    constructor() {
        this.errorMessage = "Error in Team Data Service: ";
    }
    async getTeams() {
        try {
            return await http.get("/users/team/");
        }
        catch (err) {
            throw new Error(err.response.data.message);
        }
    }
    async getSupervisor() {
        try {
            return await http.get("/users/team/supervisors/");
        }
        catch (err) {
            throw new Error(err.response.data.message);
        }
    }
}
const teamDataService = new TeamDataService();
export default teamDataService;
//# sourceMappingURL=TeamDataService.js.map