import type { eventNameType, eventItemType } from "./types"
import { v4 as uuidv4 } from "uuid";

class Event {
    // to create the events list
    public eventsItems(eventName: eventNameType, events: any, date: Date): eventItemType[] {
        let items = [];
        for (const event of events) {
            items.push(this.eventItem(eventName, event, date));
        }
        return items;
    }
    // to create the event item
    private eventItem(eventName: eventNameType, event: any, date: Date): eventItemType {
        const id: string = uuidv4();

        return {
            id: id,
            title: '🎉'+event.name ,
            description: event.description,
            date: date,
            len: 1,
            people: event.people,
            className: "task--info",
            eventName: eventName,

        }
    }
}


export default Event;