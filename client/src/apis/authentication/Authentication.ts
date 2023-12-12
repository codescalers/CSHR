import httpAxios from "../../utils/axios";
import type { loginDataType, refreshData } from "../../utils/types";

class Authentication {
  async refresh(refresh: string): Promise<refreshData> {
    // Request for getting a refresh token when token expires.
    try {
      return (
        await httpAxios.post("/auth/token/refresh/", { refresh: refresh })
      ).data;
    } catch (error: any) {
      throw new Error(error);
    }
  }

  async login(email: string, password: string) {
    // Request for getting an access token to user with his credentials.
    const loginData: loginDataType = { email: email, password: password };
    try {
      return await (
        await httpAxios.post("auth/login/", loginData)
      ).data;
    } catch (error: any) {
      console.log(error);
      
      throw new Error(
        error.response.data ? error.response.data.detail || error.response.data.message : error.message
      );
    }
  }
}

const authenticationAPI = new Authentication();
export default authenticationAPI;
