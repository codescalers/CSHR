import http from "../http-common";
class TeamDataService {
    errorMessage: string = "Error in Team Data Service: ";
    public async get(): Promise<{ results: any[], count: number, next: string, previous: string }> {
        try {
            const { data, status, statusText } = (await http.get(`/users/teams/`));
            if (status !== 200) {
                throw new Error("Error in getting team with status " + status + " wtih status text : " + statusText);
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