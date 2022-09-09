import { Writable, writable } from "svelte/store";
import type { SettingsInterface, UserInterface } from "./types";


export const SettingsStore: Writable<SettingsInterface> = writable({ "primary-color": "#aaaa", "secondary-color": "#EDF2F9", "background-image": "url('https://wallpaperaccess.com/full/2159209.jpg')" });
export const AllUsersStore: Writable<any> = writable([]);
export const UserStore: Writable<UserInterface> = writable({
    full_name: "Tiago Vilas Boas",
    phone_number: "11 972393003",
    email: "tcarvalhovb@gmail.com",
    image: "https://avatars.githubusercontent.com/u/11314585?v=4",
    role: "admin",
    id: 1,
    password: "123456"

})
