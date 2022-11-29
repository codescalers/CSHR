import Authentication from "./Authentication";
import JWTPars from "./JWTPars";
import type { IAuthStore, refreshData } from "../../utils/types";


export default async function isAuthenticated() {
	/// This is a helper function that returns the tokens if the user is authenticated. refreshes the token if expired
	let expaccess: number;
	let exprefresh: number;
	let myAuth: IAuthStore;

	const accesstoken = localStorage.getItem("accesstoken");
	const refreshtoken = localStorage.getItem("refreshtoken");

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
			const myloggingData: refreshData = await Authentication.refresh(
				refreshtoken
			);
			return (myAuth = {
				token: myloggingData.access,
				refreshtoken: myloggingData.refresh,
			});
		}

		localStorage.removeItem("refreshtoken");
		return (myAuth = { token: undefined, refreshtoken: undefined });
	}
}
