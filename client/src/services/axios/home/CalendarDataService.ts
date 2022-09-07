import http from "../http-common";
import itemHandler from "./ItemHandler"
import type { eventNameType, meetingItemType, eventItemType, vacationItemType, birthDateItemType } from "./types"


class CalendarDataService {

    private itemHandler = itemHandler;

    private async getByMonthYearAPI(month: number, year: number) {
        try {
            return await (await http.get(`/home/?month=${month}&year=${year}`)).data;
        }
        catch (error) {
            throw new Error(`Error while fetching Calendar data ${error}`);
        }
    }


    public async initCalendar() {
        let now = new Date();
        let year = now.getFullYear(); //	this is the month & year displayed
        let month = now.getMonth();


        console.log("today", month + 1, year)
        const { data } = (await this.getByMonthYearAPI(month + 1, year));
        console.log("datam", data["6"]);

        let meetings: meetingItemType[] = [];
        let events: eventItemType[] = [];
        let vacations: vacationItemType[] = [];
        let birthdates: birthDateItemType[] = [];

        for (const dayStr in data) {
            let day: number = +dayStr;
            let date = new Date(year, month, day);

            for (let eventName in data[dayStr + ""]) {
                eventName = eventName as eventNameType;
                let eventArr = data[dayStr + ""][eventName];
                switch (eventName) {
                    case "events":
                        events = [...events, ...this.itemHandler.createEventsItems(eventName, eventArr, date)];
                        break;
                    case "vacations":
                        vacations = [...vacations, ...this.itemHandler.createVacationsItems(eventName, eventArr, date)];
                        break;
                    case "birthdates":
                        birthdates = [...birthdates, ...this.itemHandler.birthDate.birthDateItem(eventName, eventArr, date)]
                        break;
                    case "meetings":
                        meetings = [...meetings, ...this.itemHandler.meeting.meetingsItems(eventName, eventArr)];
                        break;
                    default:
                        throw new Error(`Invalid event name in itemHandler ${eventName}`);
                }
            }
        }
        return [
            { meetings: meetings, className: this.cssClassMapping("meetings") },
            { events: events, className: this.cssClassMapping("events") },
            { vacations, className: this.cssClassMapping("vacations") },
            { birthdates, className: this.cssClassMapping("birthdates") }
        ];
    }





    private cssClassMapping(eventName: eventNameType): string {
        switch (eventName) {
            case "events":
                return "task--primary";
            case "meetings":
                return "task--primary";
            case "vacations":
                return "task--primary";
            case "birthdates":
                return "birthdates";
            default:
                throw new Error(`Invalid event name in itemHandler ${eventName}`);
        }

        return "";
    }
}

const calendarDataService = new CalendarDataService();

export default calendarDataService;