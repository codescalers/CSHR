import { Writable, writable } from "svelte/store";
import type {SettingsType } from "./types";


export const SettingsStore: Writable<SettingsType> = writable({ "name": null, "email": null, "primary-color": "#aaaa", "secondary-color": "#eee", "background-image": "url('https://wallpaperaccess.com/full/2159209.jpg')" });
