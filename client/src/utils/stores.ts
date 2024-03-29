import { get, type Writable, writable } from "svelte/store";

import isAuthenticated from "../apis/authentication/IsAuthenticated";
import Users from "../apis/users/users";
import type {
  GeneralUserInterface,
  IAuthStore,
  NotifacationCreatedInterface,
  NotificationType,
  OfficeType,
  PaginatedInterface,
  SettingsInterface,
  SupervisorType,
  TeamType,
  UserInterface
} from "./types";

export const SettingsStore: Writable<SettingsInterface> = writable({
  "primary-color": "#aaaa",
  "secondary-color": "#EDF2F9",
  "background-image": "url('https://wallpaperaccess.com/full/2159209.jpg')"
});

export const AllUsersStore: Writable<GeneralUserInterface[]> = writable([]);
export const UserStore: Writable<UserInterface> = writable();

export const OfficeStore: Writable<OfficeType[]> = writable([]);
export const NotificationStore: Writable<NotificationType[]> = writable([
  { id: 1 }
]);

export const TeamStore: Writable<PaginatedInterface<TeamType>> = writable();
export const NotifacationStore: Writable<NotifacationCreatedInterface> =
  writable();
export const SupervisorStore: Writable<PaginatedInterface<SupervisorType>> =
  writable();

function createAuthStore() {
  const store = writable<IAuthStore>({});
  const { subscribe, update } = store;

  isAuthenticated().then((res) => {
    if (res && res.token && res.refreshtoken) {
      updateTokens(res.token, res.refreshtoken);
    } else {
      return update((s) => {
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
      if (get(UserStore) === undefined) {
        Users.getMyProfile().then((data: UserInterface) => {
          UserStore.set({
            id: data.id,
            gender: data.gender,
            background_color: data.background_color,
            first_name: data.first_name,
            last_name: data.last_name,
            email: data.email,
            full_name: data.full_name,
            image: data.image,
            telegram_link: data.telegram_link,
            birthday: data.birthday,
            location: data.location,
            skills: data.skills,
            user_certificates: data.user_certificates,
            reporting_to: data.reporting_to,
            created_at: data.created_at,
            social_insurance_number: data.social_insurance_number,
            team: data.team,
            user_company_properties: data.user_company_properties,
            salary: data.salary,
            mobile_number: data.mobile_number,
            user_evaluation: data.user_evaluation,
            job_title: data.job_title,
            address: data.address,
            user_type: data.user_type,
            is_active: data.is_active
          });
        });
      }
    }

    return update((s) => {
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
    }
  };
}

export const authStore = createAuthStore();
