import type { eventNameType, eventItemType } from "./types"
import { v4 as uuidv4 } from "uuid";

class Event {
    // to create the events list
    public eventsItems(eventName: eventNameType, events: any, date: Date): eventItemType[] {
        let items: eventItemType[] = [];
        for (const event of events) {
            items = [...items, ...(this.eventItem(eventName, event))];
        }
        return items;
    }

    private lastDayOFWeek(startDate: Date): Date {
        const lastDay = new Date(startDate.setDate((startDate.getDate() - startDate.getDay()) + 6));
        return lastDay;
    }

    // start 5amees
    // end 7ad
    // length 3


    // to create the event item
    private eventItem(eventName: eventNameType, event: any): eventItemType[] {

        let { year: fromYear, month: fromMonth, day: fromDay, hour: fromHour, minute: fromMinute } = (event.from_date);

        let original_from_date = new Date(fromYear, Number(fromMonth) - 1, fromDay);
        let clone_from_date = new Date(fromYear, Number(fromMonth) - 1, fromDay);
        let incremental_from_date = new Date(fromYear, Number(fromMonth) - 1, fromDay);
        let weekly_from_date = new Date(fromYear, Number(fromMonth) - 1, fromDay);
        let { year: endYear, month: endMonth, day: endDay, hour: endHour, minute: endMinute } = (event.end_date);

        let end_date = new Date(endYear, Number(endMonth) - 1, endDay);
        const lastDay = this.lastDayOFWeek(clone_from_date);
        let items: eventItemType[] = [];
        let length = 0;
        for (; true === true;) {
            if (incremental_from_date.getDate() < end_date.getDate() && incremental_from_date.getDate() < lastDay.getDate()) {
                length += 1;
                incremental_from_date.setDate(incremental_from_date.getDate() + 1);
            }
            else if (incremental_from_date.getDate() === end_date.getDate() || incremental_from_date.getDate() === lastDay.getDate()) {
                length += 1;
                items = [...items,
                {
                    id: uuidv4(),
                    title: '🎉' + event.name,
                    description: event.description,
                    date: weekly_from_date,
                    from_time: fromHour + ":" + fromMinute,
                    end_time: endHour + ":" + endMinute,
                    len: length,
                    from_date: original_from_date,
                    end_date: end_date,
                    people: event.people,
                    className: "task--info",
                    eventName: eventName,
                }]
                if (incremental_from_date.getDate() === end_date.getDate()) {
                    break;
                }
                incremental_from_date.setDate(incremental_from_date.getDate() + 1);
                weekly_from_date = new Date((incremental_from_date));
                lastDay.setDate(lastDay.getDate() + 7);
                length = 0;
            }
        }
        return items;

        /*     for (; (from_date.getDate() - lastDay.getDate()) - difference <= 0;) {
                difference =
                    lastDay.setDate(lastDay.getDate() + 6);
                items.push(
                    {
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
    
                    }
                )
            }
    

        let start = lastDay.getDate() - from_date.getDate();
        let end = end_date.getDate() - lastDay.getDate();
        //alert(` from ${from_date}\\\\\\\\ end date ${end_date} \\\\\\  last day ${lastDay} \\\\ start length ${start} \\\\ end length ${end}  \\\\ diff ${end_date.getDate() - from_date.getDate() + 1}`);

        //alert(` from ${from_date}\\\\ end ${end_date} length ${end_date.getDate() - from_date.getDate() + 1} start ${start - 1} end ${end} last day ${lastDay}`)
        if (end <= 0) {
          return [{
                id: id,
                title: '🎉' + event.name,
                description: event.description,
                date: from_date,
                from_time: fromHour + ":" + fromMinute,
                end_time: endHour + ":" + endMinute,
                len: end_date.getDate() - from_date.getDate() + 1,
                from_date: from_date,
                end_date: end_date,
                people: event.people,
                className: "task--info",
                eventName: eventName,

            }]
        }

        else {
            lastDay.setDate(lastDay.getDate() + 1)

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
                from_date: from_date,
                end_date: end_date,
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
                from_date: from_date,
                end_date: end_date,
            },]
        } */
    }
}


export default Event;