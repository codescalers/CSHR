import { json } from "stream/consumers"; import http from "../http-common";
import type {loginDataType} from "./types";
 

class LoginDataService {
     
	async login(email: string, password: string) {
		const loginData :loginDataType={email:email,password:password};
       
       
		try {
			return await (await http.post("/auth/login/",loginData)).data.data;
            
		}
		catch (error) {
			throw new Error(`Error while logging in ${error}`);
		}
	}
}

    

const loginDataService = new LoginDataService();

export default loginDataService;