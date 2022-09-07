import type { eventNameType, userType, birthDateItemType } from "./types"
import { v4 as uuidv4 } from "uuid";

export default class BirthDate {
    private date: Date;
    // to create the birthdates Item
    public birthDateItem(eventName: eventNameType, events: any[]): birthDateItemType[] {
        const id: string = uuidv4();

        let user: userType;
        let users: userType[] = [];
        for (const event of events) {
            user = {
                full_name: event["full_name"], email: event["email"], image: event["image"]
            }
            users = [...users, user];
        }
        return [{
            id: id,
            title: eventName,
            users: users,
            date: this.date,
            len: 1,
        }];
    }

    // to set the date
    public set setDate(date: Date) {
        this.date = date;
    }
}