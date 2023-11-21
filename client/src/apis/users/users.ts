import type { AdminViewInterface, UserInterface, SupervisorViewInterface, registeringData, UserOptionsFilter } from './../../utils/types';
import http from "../../utils/axios";
import type { UserType } from "../../utils/types";



class Users {
	errorMessage = "Error in Users Data Service:  with status ";
	public async getAll(usersOptions?: UserOptionsFilter) {
		try {
			const { data, status, statusText } = await http.get(`/users/?location_id=${usersOptions.locationId}`);
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

	public async getOfficeUsers() {
		try {
			const { data, status, statusText } = await http.get("/users/admin/office_users/");
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

	public async getUserByID(id: number): Promise<UserInterface> {
		// Request to get user based on his user id.
		try {
			return await (
				await http.get(`/users/${id}`)
			).data.results;
		} catch (error) {
			throw new Error(error.response.data.message || error.response.data.detail);
		}
	}

	public async getByIdBasedOnUserType(
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

	public async getUserDocuments(id: number) {
        // Get the user documents.
		try {
			return await (
				await http.get(`/hr_letters/docs/${id}/`)
			).data.results;
		} catch (error) {
			throw new Error(error.response.data.message || error.response.data.detail);
		}
	}

	public async getMyProfile() {
        // Request to get user profile.
		try {
			return await (
				await http.get("myprofile/")
			).data.results;
		} catch (error) {
			throw new Error(error.response.data.message || error.response.data.detail);
		}
	}

	public async postUserDocument(data: {
		user: number;
		name: string;
		image: string;
	}) {
        // Requset to post user document.
		try {
			await http.post("hr_letters/docs/", data);
		} catch (error) {
			throw new Error(error.response.data.message || error.response.data.detail);
		}
	}

	public async changePassword(data: {
		old_password: string;
		new_password: string;
	}) {
        // Request to change request user password. 
		try {
			await http.put("/auth/change-password/", data);
		} catch (error) {
			throw new Error(`Error while registering${error}`);
		}
	}

	public async birthdates(month: number, day: number) {
        // Request to change request user password. 
		try {
			return await http.get(`/users/birthdates/?month=${month}&&day=${day}`);
		} catch (error) {
			throw new Error(`Error while registering${error}`);
		}
	}

	async register(registerData: registeringData) {
		// Register new user.
		try {
			return await (
				await http.post("/auth/signup/", JSON.stringify(registerData))
			).data;
		} catch (error) {
			throw new Error(`Error while registering${error}`);
		}
	}

	async updateProfile(registerData: UserInterface) {
		// Update user profile
		try {
			return await (
				await http.put(`/myprofile/update/profile/${registerData.id}/`, JSON.stringify(registerData))
			).data;
		} catch (error) {
			throw new Error(`Error while registering${error}`);
		}
	}

	async setAsActive(userID: number) {
		// Update user profile
		try {
			return await (
				await http.put(`/users/set_active/`, JSON.stringify({"user_id": userID}))
			).data;
		} catch (error) {
			throw new Error(`Error while setting user as active user due: ${error}`);
		}
	}

	async setAsInactive(userID: number) {
		// Update user profile
		try {
			return await (
				await http.put(`/users/set_inactive/`, JSON.stringify({"user_id": userID}))
			).data;
		} catch (error) {
			throw new Error(`Error while setting user as an inactive user due: ${error}`);
		}
	}
}

const usersAPI = new Users();
export default usersAPI;
