import type {
	AdminViewInterface,
	SupervisorViewInterface,
	UserInterface,
	UserType,
} from "../../../types";
import http from "../http-common";
class UsersDataService {
	errorMessage = "Error in Users Data Service:  with status ";
	public async getAll() {
		try {
			const { data, status, statusText } = await http.get("/users/");
			if (status === 404) {
				throw new Error("Users not found");
			} else if (status !== 200) {
				throw new Error(
					this.errorMessage + status + " wtih status text : " + statusText
				);
			}
			return data.results;
		} catch (error) {
			console.error(error);
			throw new Error(error);
		}
	}
	public async getById(
		id: number,
		user_type: UserType
	): Promise<UserInterface | AdminViewInterface | SupervisorViewInterface> {
		try {
			const { data, status, statusText } = await http.get(
				`/users/${
					user_type === "User" ? "" : user_type.toLowerCase() + "/"
				}${id}/`
			);
			if (status === 404) {
				throw new Error("User not found");
			} else if (status !== 200) {
				throw new Error(
					this.errorMessage + status + " wtih status text : " + statusText
				);
			}
			return data.results;
		} catch (error) {
			console.error(error);
			throw new Error(error);
		}
	}
}

const usersDataService = new UsersDataService();
export default usersDataService;
