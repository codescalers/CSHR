import http from "../http-common";
class UserDataService {
	errorMessage = "Error in User Data Service: ";

	public async getById(id: number) {
		try {
			return await (
				await http.get(`/users?id=${id}`)
			).data;
		} catch (err) {
			console.error(this.errorMessage + err);
		}
	}
	public async getUserDocuments(id: number) {
		try {
			return await (
				await http.get(`/hr_letters/docs/${id}/`)
			).data.results;
		} catch (err) {
			console.error(this.errorMessage + err);
		}
	}

	public async getMyProfile() {
		try {
			return await (
				await http.get("myprofile/")
			).data.results;
		} catch (err) {
			console.error(this.errorMessage + err);
		}
	}
	public async postUserDocument(data: {
		user: number;
		name: string;
		image: string;
	}) {
		try {
			await http.post("hr_letters/docs/", data);
		} catch (err) {
			console.error(this.errorMessage + err);
		}
	}
	public async changePassword(data: {
		old_password: string;
		new_password: string;
	}) {
		try {
			const { status, statusText } = await http.put("/auth/change-password/", data);
			if (status === 404) {
				throw new Error("User not found");
			} else if (status !== 200) {
				throw new Error(
					this.errorMessage + status + " wtih status text : " + statusText
				);
			};
			
		} catch (err) {
			throw new Error(`Error while registering${err}`);
		}
	}
}

const userDataService = new UserDataService();
export default userDataService;
