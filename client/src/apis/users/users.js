import http from "../../utils/axios";
class Users {
    constructor() {
        this.errorMessage = "Error in Users Data Service:  with status ";
    }
    async getAll(usersOptions) {
        try {
            const { data, status, statusText } = await http.get(`/users/?location_id=${usersOptions ? usersOptions.locationId : ""}`);
            if (status === 404) {
                throw new Error("Users not found");
            }
            else if (status !== 200) {
                throw new Error(this.errorMessage + status + " wtih status text : " + statusText);
            }
            return data.results;
        }
        catch (error) {
            console.error(error);
            throw new Error(error);
        }
    }
    async getOfficeUsers() {
        try {
            const { data, status, statusText } = await http.get("/users/admin/office_users/");
            if (status === 404) {
                throw new Error("Users not found");
            }
            else if (status !== 200) {
                throw new Error(this.errorMessage + status + " wtih status text : " + statusText);
            }
            return data.results;
        }
        catch (error) {
            console.error(error);
            throw new Error(error);
        }
    }
    async getUserByID(id) {
        // Request to get user based on his user id.
        try {
            return await (await http.get(`/users/${id}`)).data.results;
        }
        catch (error) {
            throw new Error(error.response.data.message || error.response.data.detail);
        }
    }
    async getByIdBasedOnUserType(id, user_type) {
        try {
            const { data, status, statusText } = await http.get(`/users/${user_type === "User" ? "" : user_type.toLowerCase() + "/"}${id}/`);
            if (status === 404) {
                throw new Error("User not found");
            }
            else if (status !== 200) {
                throw new Error(this.errorMessage + status + " wtih status text : " + statusText);
            }
            return data.results;
        }
        catch (error) {
            console.error(error);
            throw new Error(error);
        }
    }
    async getUserDocuments(id) {
        // Get the user documents.
        try {
            return await (await http.get(`/hr_letters/docs/${id}/`)).data.results;
        }
        catch (error) {
            throw new Error(error.response.data.message || error.response.data.detail);
        }
    }
    async getMyProfile() {
        // Request to get user profile.
        try {
            return await (await http.get("myprofile/")).data.results;
        }
        catch (error) {
            throw new Error(error.response.data.message || error.response.data.detail);
        }
    }
    async postUserDocument(data) {
        // Requset to post user document.
        try {
            await http.post("hr_letters/docs/", data);
        }
        catch (error) {
            throw new Error(error.response.data.message || error.response.data.detail);
        }
    }
    async changePassword(data) {
        // Request to change request user password.
        try {
            await http.put("/auth/change-password/", data);
        }
        catch (error) {
            throw new Error(`Error while registering${error}`);
        }
    }
    async birthdates(month, day) {
        // Request to change request user password.
        try {
            return await http.get(`/users/birthdates/?month=${month}&&day=${day}`);
        }
        catch (error) {
            throw new Error(`Error while registering${error}`);
        }
    }
    async register(registerData) {
        // Register new user.
        try {
            return await (await http.post("/auth/signup/", JSON.stringify(registerData))).data;
        }
        catch (error) {
            throw new Error(`Error while registering${error}`);
        }
    }
    async updateProfile(registerData) {
        // Update user profile
        try {
            return await (await http.put(`/myprofile/update/profile/${registerData.id}/`, JSON.stringify(registerData))).data;
        }
        catch (error) {
            throw new Error(`Error while registering${error}`);
        }
    }
    async setAsActive(userID) {
        // Update user profile
        try {
            return await (await http.put(`/users/set_active/`, JSON.stringify({ user_id: userID }))).data;
        }
        catch (error) {
            throw new Error(`Error while setting user as active user due: ${error}`);
        }
    }
    async setAsInactive(userID) {
        // Update user profile
        try {
            return await (await http.put(`/users/set_inactive/`, JSON.stringify({ user_id: userID }))).data;
        }
        catch (error) {
            throw new Error(`Error while setting user as an inactive user due: ${error}`);
        }
    }
}
const usersAPI = new Users();
export default usersAPI;
//# sourceMappingURL=users.js.map