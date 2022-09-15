import type { SettingsType } from "../../types";
import { SettingsStore } from "../../stores";

class SettingsApi {

    public getSettings(): SettingsType {
        const settings: SettingsType = {
            name: localStorage.getItem("name"),
            email: localStorage.getItem("email"),
            "primary-color": localStorage.getItem("primary-color") || "#2B515F",
            "secondary-color": localStorage.getItem("secondary-color") || "#EDF2F9",
        }
        return settings;
    }


    public setSettings(settings: SettingsType): void {
        localStorage.setItem("name", settings.name);
        localStorage.setItem("email", settings.email);
        localStorage.setItem("primary-color", settings["primary-color"]);
        localStorage.setItem("secondary-color", settings["secondary-color"]);
        this.updateSettings();
    }
    public updateSettings(): void {
        const settings: SettingsType = {
            name: localStorage.getItem("name"),
            email: localStorage.getItem("email"),
            "primary-color": localStorage.getItem("primary-color") || "#aaaa",
            "secondary-color": localStorage.getItem("secondary-color") || "#EDF2F9",
        }
        SettingsStore.set(settings);
    }
    public isName(): boolean {
        return localStorage.getItem("name") !== null;
    }
    public getName(): string {
        return localStorage.getItem("name");
    }
}

export default new SettingsApi();