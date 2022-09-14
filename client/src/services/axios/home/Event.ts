import type { eventNameType, eventItemType } from "./types"
import { v4 as uuidv4 } from "uuid";

class Event {
    // to create the events list
    public eventsItems(eventName: eventNameType, events: any, date: Date): eventItemType[] {
        let items: eventItemType[] = [];
        for (const event of events) {
            items = [...items, ...(this.eventItem(eventName, event, date))];
        }
        return items;
    }

    private lastDayOFWeek(): Date {
        const today = new Date();
        const lastDay = new Date(today.setDate(today.getDate() - today.getDay() + 6));

        return lastDay;
    }

    // to create the event item
    private eventItem(eventName: eventNameType, event: any, date: Date): eventItemType[] {
        const id: string = uuidv4();

        let { year: fromYear, month: fromMonth, day: fromDay, hour: fromHour, minute: fromMinute } = (event.from_date);
        let from_date = new Date(fromYear, Number(fromMonth) - 1, fromDay);
        let { year: endYear, month: endMonth, day: endDay, hour: endHour, minute: endMinute } = (event.end_date);
        let end_date = new Date(endYear, Number(endMonth) - 1, endDay);
        const lastDay = this.lastDayOFWeek();

        let start = lastDay.getDate() - from_date.getDate();
        let end = end_date.getDate() - lastDay.getDate();

        if (end <= 0) {
            alert("from " + from_date + " end" + end_date + "lengt " + (end_date.getDate() - from_date.getDate() + 1));
            return [{
                id: id,
                title: '🎉' + event.name,
                description: event.description,
                date: from_date,
                from_time: fromHour + ":" + fromMinute,
                end_time: endHour + ":" + endMinute,
                len: end_date.getDate() - from_date.getDate() + 1,
                people: event.people,
                className: "task--info",
                eventName: eventName,

            }]
        }
        else {
            lastDay.setDate(lastDay.getDate() + 1)
            alert(` from ${from_date}\\\\ end ${end_date} length ${end_date.getDate() - from_date.getDate() + 1} start ${start - 1} end ${end} last day ${lastDay}`)

            return [{
                id: id,
                title: '🎉' + event.name,
                description: event.description,
                date: from_date,
                len: start - 1,
                people: event.people,
                className: "task--info",
                eventName: eventName,
                from_time: fromHour + ":" + fromMinute,
                end_time: endHour + ":" + endMinute,
            }, {
                id: uuidv4(),
                title: '',
                description: event.description,
                date: lastDay,
                len: end,
                people: event.people,
                className: "task--info",
                eventName: eventName,
                from_time: fromHour + ":" + fromMinute,
                end_time: endHour + ":" + endMinute,
            },]
        }
    }
}


export default Event;