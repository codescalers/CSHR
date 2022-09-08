import type { eventNameType, userType, birthDateItemType } from "./types"
import { v4 as uuidv4 } from "uuid";

export default class BirthDate {
    // to create the birthdates Item
    public birthDateItem(eventName: eventNameType, events: any[], date: Date): birthDateItemType[] {
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
            title: "🎂birthday" + (users.length > 1 ? "s" : ""),
            users: users,
            date: date,
            len: 1,
            className: "task--primary",
            eventName: eventName,
            isStart: true,
            isBottom: false,
        }];
    }


}