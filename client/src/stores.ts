import { Writable, writable, get } from "svelte/store";
import isAuthenticated from "./services/authentication/IsAuthenticated";
import parseJwt from "./services/authentication/JWTPars";
import userDataService from "./services/axios/user/UserDataService";
import type {
	SettingsInterface,
	AdminViewType,
	OfficeType,
	NotificationType,
	TeamType,
	PaginatedInterface,
	IAuthStore
} from "./types";

export const SettingsStore: Writable<SettingsInterface> = writable({
	"primary-color": "#aaaa",
	"secondary-color": "#EDF2F9",
	"background-image": "url('https://wallpaperaccess.com/full/2159209.jpg')",
});
export const AllUsersStore: Writable<AdminViewType[]> = writable([]);
export const UserStore: Writable<AdminViewType> = writable();

export const OfficeStore: Writable<OfficeType[]> = writable([]);
export const NotificationStore: Writable<NotificationType[]> = writable([
	{ id: 1 },
]);

export const TeamStore: Writable<PaginatedInterface<TeamType>> = writable();

function createAuthStore() {
     
	const store = writable<IAuthStore>({
    
	});
	const user = get(UserStore);
	const { subscribe, update } = store;

	isAuthenticated().then(res=>{ 
		if(res&& res.token && res.refreshtoken){
			updateTokens(res.token, res.refreshtoken);
		}
		else{
			return update(s => {
				s.token = undefined;
				s.refreshtoken = undefined;
				return s;
			});
		}
	});


	function updateTokens(token: string, refresh: string): void {
       
		localStorage.setItem("accesstoken", token);
         
		localStorage.setItem("refreshtoken", refresh);

		if (token) {
			if (UserStore === undefined){
            userDataService.getMyProfile().then(data=>{
				UserStore.set({
				    full_name: string;
                    email: string;
                    mobile_number: string;
                    team: string;
                    password?: string;
                    user_type:string;
                    role: string;
                    image: string;
                    gender: "Female" | "Male";
                    address: string;
                    birthday: string;
                    CreatedAt?: string;
                    UpdatedAt?: string;
                    DeletedAt?: string;
                    job_title: string;
                    telegram_link: string;
                    skills: SkillType[];
                    user_certificates: CertificateType[];
                    reporting_to: number[];

				});
			})}
		}

		return update(s => {
			s.token = token;
			s.refreshtoken = refresh;
            
			return s;
		});
       
        
	}

    

	return {
		subscribe,
		updateTokens,
		isAuth(): boolean {
			const { token, refreshtoken } = get(store);
			return !!token && !!refreshtoken;

		},
		isAdmin():boolean{
			const { token, refreshtoken } = get(store);
			return !!token && !!refreshtoken && user.user_type==="Admin";
		},

		isSupervisor():boolean{
			const { token, refreshtoken } = get(store);
			return !!token && !!refreshtoken && user.user_type==="Supervisor";
		}
	};
}


export const authStore = createAuthStore();
