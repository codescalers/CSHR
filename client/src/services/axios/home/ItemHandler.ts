import type {
	eventNameType,
	eventItemType,
	meetingItemType,
	birthDateItemType,
	vacationItemType,
} from "./types";
import Vacation from "./Vacation";
import BirthDate from "./Birthdate";
import Event from "./Event";
import Meeting from "./Meeting";

class ItemHandler {
	vacation: Vacation = new Vacation();
	birthDate = new BirthDate();
	event = new Event();
	meeting = Meeting;

	public createEventsItems(
		eventName: eventNameType,
		event: any,
		date: Date
	): eventItemType[] {
		return this.event.eventsItems(eventName, event, date);
	}

	public createBirthdatesItems(
		eventName: eventNameType,
		event: any,
		date: Date
	): birthDateItemType[] {
		return this.birthDate.birthDateItem(eventName, event, date);
	}

	public createVacationsItems(
		eventName: eventNameType,
		event: any,
		date: Date
	): vacationItemType[] {
		return this.vacation.vacationsItems(eventName, event, date);
	}

	public createMeetingsItems(
		eventName: eventNameType,
		event: any,
		date: Date
	): meetingItemType[] {
		return this.meeting.meetingsItems(eventName, event, date);
	}
}

const itemHandler = new ItemHandler();
export default itemHandler;
