import type { eventNameType, userType, birthDateItemType, calendarItemType } from "./types"
import Vacation from "./Vacation";
import BirthDate from "./Birthdate";
import Event from "./Event";
import { v4 as uuidv4 } from "uuid";

class ItemHandler {
    date: Date;
    vacation: Vacation = new Vacation(this.cssClassMapping);
    birthDate = new BirthDate(this.cssClassMapping);
    event = new Event(this.cssClassMapping);
    public createItems(eventName: eventNameType, event: any, date: Date): calendarItemType[] {
        this.date = date;
        let items: calendarItemType[] = [];
        console.log(eventName);
        console.log(event);

        switch (eventName) {
            case "events":
                this.event.setDate = this.date;
                items = [...items, ...this.event.eventsItems(eventName, event)];
                break;
            case "vacations":
                this.vacation.setDate = date;
                items = [...items, ...this.vacation.vacationsItems(eventName, event)];
                break;
            case "birthdates":
                this.birthDate.setDate = date;
                items = [...items, ...this.birthDate.birthDateItem(eventName, event)];
                break;
            case "meetings":
                items = [...items, ...this.meetings(eventName, event)];
                break;

            default:
                throw new Error(`Invalid event name in itemHandler ${eventName}`);
        }

        console.log("items++", items);
        return items;
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
            case "events":
                return "task--primary";
            case "tasks":
                return "task--primary";
            case "meetings":
                return "task--primary";
            case "vacations":
                return "task--primary";
            case "birthdates":
                return "birthdates";
            case "other":
                return "task--primary";
            default:
                throw new Error(`Invalid event name in itemHandler ${eventName}`);
        }

        return "";
    }
}




const itemHandler = new ItemHandler();
export default itemHandler;