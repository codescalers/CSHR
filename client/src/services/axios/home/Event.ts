import type { eventNameType, eventItemType } from "./types";
import { v4 as uuidv4 } from "uuid";

class Event {
	// to create the events list
	public eventsItems(
		eventName: eventNameType,
		events: any,
		date: Date
	): eventItemType[] {
		let items: eventItemType[] = [];
		for (const event of events) {
			items = [...items, ...this.eventItem(eventName, event)];
		}
		return items;
	}

	private lastDayOFWeek(startDate: Date): Date {
		const lastDay = new Date(
			startDate.setDate(startDate.getDate() - startDate.getDay() + 6)
		);
		return lastDay;
	}

	// start 5amees
	// end 7ad
	// length 3

	// to create the event item
	private eventItem(eventName: eventNameType, event: any): eventItemType[] {
		const {
			year: fromYear,
			month: fromMonth,
			day: fromDay,
			hour: fromHour,
			minute: fromMinute,
		} = event.from_date;

		const original_from_date = new Date(fromYear, Number(fromMonth) - 1, fromDay);
		const clone_from_date = new Date(fromYear, Number(fromMonth) - 1, fromDay);
		const incremental_from_date = new Date(
			fromYear,
			Number(fromMonth) - 1,
			fromDay
		);
		let weekly_from_date = new Date(fromYear, Number(fromMonth) - 1, fromDay);
		const {
			year: endYear,
			month: endMonth,
			day: endDay,
			hour: endHour,
			minute: endMinute,
		} = event.end_date;

		const end_date = new Date(endYear, Number(endMonth) - 1, endDay);
		const lastDay = this.lastDayOFWeek(clone_from_date);
		let items: eventItemType[] = [];
		let length = 0;
		for (; true === true; ) {
			if (
				incremental_from_date.getDate() < end_date.getDate() &&
        incremental_from_date.getDate() < lastDay.getDate()
			) {
				length += 1;
				incremental_from_date.setDate(incremental_from_date.getDate() + 1);
			} else if (
				incremental_from_date.getDate() === end_date.getDate() ||
        incremental_from_date.getDate() === lastDay.getDate()
			) {
				length += 1;
				items = [
					...items,
					{
						id: uuidv4(),
						title: "🎉" + event.name,
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
					},
				];
				if (incremental_from_date.getDate() === end_date.getDate()) {
					break;
				}
				incremental_from_date.setDate(incremental_from_date.getDate() + 1);
				weekly_from_date = new Date(incremental_from_date);
				lastDay.setDate(lastDay.getDate() + 7);
				length = 0;
			}
		}
		return items;
	}
}

export default Event;
