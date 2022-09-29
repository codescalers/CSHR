import type { loggingData, refreshData } from "../axios/login/types";
import refreshDataService from "../axios/login/UserRefreshService";
import JWTPars from "./JWTPars";
import type { IAuthStore } from "../../types";
export default async function isAuthenticated() {
	/// This is a helper function that returns the tokens if the user is authenticated. refreshes the token if expired
	let expaccess;
	let exprefresh;
	const accesstoken = localStorage.getItem("accesstoken");
	const refreshtoken = localStorage.getItem("refreshtoken");
	let myAuth: IAuthStore;
	if (refreshtoken) {
		expaccess = accesstoken ? JWTPars(accesstoken).exp : null;
		exprefresh = JWTPars(refreshtoken).exp;
		if (accesstoken) {
			if (Date.now() >= expaccess * 1000) {
				localStorage.removeItem("accesstoken");
			} else if (Date.now() < exprefresh * 1000) {
				return { token: accesstoken, refreshtoken: refreshtoken };
			}
		}
		if (Date.now() < exprefresh * 1000) {
			const myloggingData: refreshData = await refreshDataService.refresh(
				refreshtoken
			);
			console.log(myloggingData);
			return (myAuth = {
				token: myloggingData.access,
				refreshtoken: myloggingData.refresh,
			});
		}
		localStorage.removeItem("refreshtoken");
		return (myAuth = { token: undefined, refreshtoken: undefined });
	}
}
