import type { eventNameType, userBirthDateType, birthDateType } from "./types"
import { v4 as uuidv4 } from "uuid";

class ItemHandler {
    date: Date;
    public createItems(eventName: eventNameType, event: any, date: Date) {
        this.date = date;
        let items: any[] = [];
        console.log(eventName);
        console.log(event);

        switch (eventName) {
            case "events":
                items = [...items, this.events(eventName, event)];
                break;
            case "birthdates":
                items = [...items, this.birthDates(eventName, event)];
                break;
            case "meetings":
                items = [...items, this.meetings(eventName, event)];
            default:
                throw new Error("Invalid event name in itemHandler");
        }
        return items;
    }

    // to create the events list
    private events(eventName: string, events: any): any[] {
        let items = [];
        for (const event of events) {
            items.push(this.eventItem(eventName, event));
        }
        return items;
    }
    // to create the event item
    private eventItem(eventName: string, event: any): {} {
        const id: string = uuidv4();

        return {
            id: id,
            title: event.name,
            description: event.description,
            date: this.date,
            len: 1,
            className: this.cssClassMapping(eventName)
        }
    }


    // to create the birthdates list
    private birthDates(eventName: string, events: any[]): birthDateType[] {
        const id: string = uuidv4();

        let user: userBirthDateType;
        let users: userBirthDateType[] = [];
        for (const event of events) {
            user = {
                full_name: event["full_name"], email: event["email"], image: event["image"]
            }
            users = [...users, user];
        }
        return [{
            id: id,
            title: eventName,
            className: this.cssClassMapping(eventName),
            users: users,
            date: this.date,
            len: 1,
        }];
    }


    // to create the meetings list
    private meetings(eventName: string, event: any): any[] {
        /*         return {
                    id: event.id,
                    title: event.name,
                    description: event.description,
                    len: 1,
                } */

        return [];
    }

    // to create the meeting Item
    private meetingItem(eventName: string, event: any) {
        const id: string = uuidv4();

        return {
            id: id,
            title: event.name,
            description: event.description,
            len: 1,
        }
    }


    private cssClassMapping(eventName: string): string {
        switch (eventName) {
            case "event":
                return "task--primary";
            case "task":
                return "task--primary";
            case "meeting":
                return "task--primary";
            case "holiday":
                return "task--primary";
            case "birthdates":
                return "birthdates";
            case "anniversary":
                return "task--primary";
            case "reminder":
                return "task--primary";
            case "other":
                return "task--primary";
        }

        return "";
    }
}




const itemHandler = new ItemHandler();
export default itemHandler;