import type { eventNameType, eventItemType } from "./types"
import { v4 as uuidv4 } from "uuid";

class Event {
    private date: Date;


    // to set the date
    public set setDate(date: Date) {
        this.date = date;
    }


    // to create the events list
    public eventsItems(eventName: eventNameType, events: any): eventItemType[] {
        let items = [];
        for (const event of events) {
            items.push(this.eventItem(eventName, event));
        }
        return items;
    }
    // to create the event item
    private eventItem(eventName: eventNameType, event: any): eventItemType {
        const id: string = uuidv4();

        return {
            id: id,
            title: event.name + " " + eventName,
            description: event.description,
            date: this.date,
            len: 1,
            people: event.people,

        }
    }
}


export default Event;