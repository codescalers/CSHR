import http from "../http-common";
import itemHandler from "./ItemHandler"
import type { eventNameType, meetingItemType, eventItemType, vacationItemType, birthDateItemType, userType } from "./types"

class CalendarDataService {

    private itemHandler = itemHandler;
    private errorMessage: string = "Error in Office Data Service: ";


    private async getByMonthYearAPI(month: number, year: number) {
        try {
            return await (await http.get(`/home/?month=${month}&year=${year}`)).data;
        }
        catch (error) {
            console.error(`${this.errorMessage} Error while fetching Calendar data ${error}`);
        }
    }
    public async postMeeting(e: { hostedUserID: number, invitedUsers: number[], time: string, meetingLink: string, date: string, location: string }) {
        try {
            if (!e.hostedUserID || !e.invitedUsers || !e.meetingLink || !e.time || !e.date) throw new Error("Invalid data");
            if (e.invitedUsers.length === 0) throw new Error("No invited users");
            if (e.invitedUsers.includes(e.hostedUserID)) throw new Error("Hosted user is also invited");
            console.log("meeting", e)
            const [hour, minute] = e.time.split(":");
            const [year, month, day] = e.date.split("-");
            alert(e.hostedUserID + "s")
            const { status } = await http.post("/meeting/", JSON.stringify({
                "host_user": e.hostedUserID,
                "invited_users": e.invitedUsers,
                "date": {
                    year: Number(year),
                    month: Number(month),
                    day: Number(day),
                    hour: Number(hour),
                    minute: Number(minute)
                },
                "meeting_link": e.meetingLink,
                "location": e.location
            }));
            if (status !== 201) {
                throw new Error("Error while posting meeting");
            }

        }
        catch (error) {
            alert(error)
            console.error(`${this.errorMessage} Error while posting meeting data ${error}`);
            return error
        }
    }


    public async postEvent(e: { description: string, name: string, people: number[], end_date: string, end_time: string, from_date: string, from_time: string, location: string }) {
        try {
            if (!e.name || !e.people || e.people.length !== 0 || !e.end_date || !e.location || !e.end_time || !e.from_time) throw new Error("Invalid data");
            if (e.people.length === 0) throw new Error("No invited users");
            const [fromHour, fromMinute] = e.from_time.split(":");
            const [fromYear, fromMonth, fromDay] = e.from_date.split("-");
            const [endHour, endMinute] = e.end_time.split(":");
            const [endYear, endMonth, endDay] = e.from_date.split("-");
            const { status } = await http.post("/meeting/", JSON.stringify({
                "people": e.people,
                "from_date": {
                    year: Number(fromYear),
                    month: Number(fromMonth),
                    day: Number(fromDay),
                    hour: Number(fromHour),
                    minute: Number(fromMinute)
                },
                "end_date": {
                    year: Number(endYear),
                    month: Number(endMonth),
                    day: Number(endDay),
                    hour: Number(endHour),
                    minute: Number(endMinute)
                },
                "name": e.name,
                "description": e.description,
                "location": e.location
            }));
            if (status !== 201) {
                throw new Error("Error while posting event with status " + status);
            }

        }
        catch (error) {
            alert(error)
            console.error(`${this.errorMessage} Error while posting event data ${error}`);
            return error
        }
    }

    public async postLeave(e: { applyingUserId: number, reason: string, end_date: string, from_date: string, location: string }) {
        try {
            if (!e.applyingUserId || !e.end_date || !e.location) throw new Error("Invalid data");
            const { status } = await http.post("/vacation/", JSON.stringify({
                "applying_user_id": e.applyingUserId,
                "from_date": e.from_date,
                "end_date": e.end_date,
                "reason": e.reason,
                "type": ""
            }));
            if (status !== 201) {
                throw new Error("Error while posting leave with status " + status);
            }

        }
        catch (error) {
            alert(error)
            console.error(`${this.errorMessage} Error while leave event data ${error}`);
            return error
        }
    }

    public async initCalendar() {
        let now = new Date();
        let year = now.getFullYear(); //	this is the month & year displayed
        let month = now.getMonth();


        console.log("today", month + 1, year)
        const { data } = (await this.getByMonthYearAPI(month + 1, year));

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
                        meetings = [...meetings, ...this.itemHandler.meeting.meetingsItems(eventName, eventArr, date)];
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
                return "task--info";
            case "birthdates":
                return " .task--warning";
            default:
                throw new Error(`Invalid event name in itemHandler ${eventName}`);
        }

        return "";
    }
}

const calendarDataService = new CalendarDataService();

export default calendarDataService;