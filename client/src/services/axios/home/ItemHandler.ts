import type { eventNameType, eventItemType, meetingItemType, birthDateItemType, vacationItemType } from "./types"
import Vacation from "./Vacation";
import BirthDate from "./Birthdate";
import Event from "./Event";
import Meeting from "./Meeting";

class ItemHandler {
    vacation: Vacation = new Vacation();
    birthDate = new BirthDate();
    event = new Event();
    meeting = Meeting;

    public createEventsItems(eventName: eventNameType, event: any, date: Date): eventItemType[] {
        this.event.setDate = date;
        return this.event.eventsItems(eventName, event);
    }


    public createBirthdatesItems(eventName: eventNameType, event: any, date: Date): birthDateItemType[] {
        this.birthDate.setDate = date;
        return this.birthDate.birthDateItem(eventName, event);
    }

    public createVacationsItems(eventName: eventNameType, event: any, date: Date): vacationItemType[] {
        this.vacation.setDate = date;
        return this.vacation.vacationsItems(eventName, event);
    }

    public createMeetingsItems(eventName: eventNameType, event: any, date: Date): meetingItemType[] {
        this.meeting.setDate = date;
        return this.meeting.meetingsItems(eventName, event);
    }


}




const itemHandler = new ItemHandler();
export default itemHandler;